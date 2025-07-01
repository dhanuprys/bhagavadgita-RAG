import json
from app.application.service.pattern_matching import PatternMatching
from app.domain.value_object.pattern_matching_result import (
    PatternMatchingResult,
    PatternMatchingContext,
)
from app.domain.value_object.attachment import Attachment
from os import getenv


class FullGitaMatching(PatternMatching):
    library_base_url = getenv("LIBRARY_BASE_URL") or "http://localhost:5173"

    def match(self, user_input: str) -> dict | None:
        prompt = """
Anda adalah AI yang bertugas sebagai 'intent classifier' yang sangat ketat dan efisien untuk chatbot Bhagavad Gita.
Tugas Anda adalah mengklasifikasikan pertanyaan pengguna ke dalam kategori yang telah ditentukan. Jika pertanyaan tidak termasuk dalam kategori yang diizinkan atau tidak memiliki informasi yang cukup (seperti nomor bab), Anda HARUS mengklasifikasikannya sebagai 'unsupported_query'.

Output wajib dalam format JSON yang valid. Output HARUS berupa string JSON mentah tanpa blok kode markdown seperti ```json atau ```.

### Kategori Aksi yang Diizinkan:

1.  `get_random_verses`: Saat pengguna meminta sloka acak tanpa terikat pada bab.
    * Parameter: `count` (integer)

2.  `get_specific_verse`: Saat pengguna meminta isi sloka tertentu dari bab spesifik.
    * Parameter: `chapter` (integer), `verse` (integer)

3.  `get_sample_verses`: Saat pengguna meminta sejumlah sloka sebagai contoh dari sebuah bab spesifik.
    * Parameter: `chapter` (integer), `count` (integer), `expandable` (boolean)

4.  `get_chapter_summary`: Saat pengguna meminta ringkasan bab, atau hanya menyebutkan nomor bab.
    * Parameter: `chapter` (integer)

5.  `get_chapter_metadata`: Saat pengguna menanyakan info spesifik tentang bab (jumlah ayat/nama bab).
    * Parameter: `chapter` (integer), `metadata_type` (string, "verse_count" atau "chapter_name")
    
6. `get_writer`: Saat pengguna menanyakan informasi pembuat/penulis kitab bhagavad gita
    * Parameter: Tidak ada parameter

7. `get_chapter_count`: Saat pengguna menanyakan jumlah bab pada kitab bhagavad gita
    * Parameter: Tidak ada parameter


### Kategori Penolakan:

1.  `unsupported_query`: Untuk SEMUA pertanyaan lain, termasuk yang tidak lengkap, sapaan, topik umum, perbandingan, atau di luar konteks.
    * Tidak ada parameter.


### Contoh Kasus:

Pertanyaan: "berikan sloka acak"
JSON:
{"action": "get_random_verses", "parameters": {"count": 1}}

Pertanyaan: "berikan 5 sloka bebas"
JSON:
{"action": "get_random_verses", "parameters": {"count": 5}}

Pertanyaan: "Tolong berikan isi dari bab 1 sloka 1."
JSON:
{"action": "get_specific_verse", "parameters": {"chapter": 1, "verse": 1}}

Pertanyaan: "sebutkan 5 sloka pada bab 10"
JSON:
{"action": "get_sample_verses", "parameters": {"chapter": 10, "count": 5, "expandable": false}}

Pertanyaan: "apa saja sloka-sloka pada bab 9"
JSON:
{"action": "get_sample_verses", "parameters": {"chapter": 9, "count": 3, "expandable": true}}

Pertanyaan: "Bab 2 dong."
JSON:
{"action": "get_chapter_summary", "parameters": {"chapter": 2}}

Pertanyaan: "Ada berapa ayat di bab 18?"
JSON:
{"action": "get_chapter_metadata", "parameters": {"chapter": 18, "metadata_type": "verse_count"}}

Pertanyaan: "Apa nama bab dari bab 18?"
JSON:
{"action": "get_chapter_metadata", "parameters": {"chapter": 18, "metadata_type": "chapter_name"}}

Pertanyaan: "siapa penulis bhagavad gita?"
JSON:
{"action": "get_writer", "parameters": {}}

Pertanyaan: "ada berapa bab dalam bhagavad gita?"
JSON:
{"action": "get_chapter_count", "parameters": {}}

Pertanyaan: "Tolong ringkasannya"
JSON:
{"action": "unsupported_query", "parameters": {}}


### Tugas Anda:

Analisis pertanyaan pengguna di bawah ini dan hasilkan JSON yang sesuai dengan aturan ketat di atas.

Pertanyaan: [QUESTION]{user_input}[/QUESTION]
JSON:
""".replace(
            "{user_input}", user_input
        )
        check_result = (
            self.app.llm_collection.intent_classifier.generate(prompt)
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        json_response = {"action": "unsupported_query", "parameters": {}}

        try:
            json_response = json.loads(check_result)
        except json.JSONDecodeError:
            return None

        if json_response["action"] == "unsupported_query":
            return None

        return json_response

    def handle(
        self, user_input: str, matching_result: dict
    ) -> PatternMatchingResult | None:
        action_type = matching_result["action"]
        parameters = matching_result["parameters"]

        if action_type == "get_writer":
            context = [
                PatternMatchingContext(
                    label="Penulis",
                    content="Rsi Vyāsa, juga dikenal sebagai Krishna Dvaipayāna atau Vedavyāsa, adalah resi legendaris dalam tradisi Hindu yang lahir di tepian Sungai Yamuna sebagai putra Parāśara dan Satyavatī. Ia digelari “Veda‑Vyāsa” karena membagi Veda tunggal menjadi empat kitab—Rig, Yajur, Sāma, dan Atharva—agar lebih mudah dipelajari dan dipahami. Ia adalah pengarang epik Mahābhārata yang sangat panjang, termasuk 700 ayat Bhagavad Gītā dalam bagian Bhīṣma Parva, yang ia diktakan kepada dewa Ganesha. Selain itu, ia menulis 18 Purāṇa, menyusun Brahma Sutra, dan dianggap sebagai avatāra parsial Wiṣṇu serta salah satu Chiranjīvi (makhluk abadi). Rsi Vyāsa juga berperan penting dalam memelihara keturunan dinasti Kuru melalui praktik niyoga, serta dihormati setiap tahun pada hari Guru Pūrṇimā sebagai guru abadi umat manusia.",
                )
            ]
            return PatternMatchingResult(type="context", context=context)
        elif action_type == "get_chapter_count":
            chapters = self.app.chapter_repository.get_all()
            context_content = ", ".join(
                [f"BAB {x.chapter_number}: {x.name}" for x in chapters]
            )
            display_content = "\n".join(
                [f"- Bab {x.chapter_number} - {x.name}" for x in chapters]
            )
            context = [
                PatternMatchingContext(
                    label="Jumlah Bab",
                    content=f"Terdapat {len(chapters)} bab Bhagavad Gita. Terdiri dari {context_content}",
                    display_content=f"Terdapat {len(chapters)} bab Bhagavad Gita. Terdiri dari:\n\n{display_content}",
                    link=f"{self.library_base_url}",
                )
            ]
            return PatternMatchingResult(type="context", context=context)
        elif action_type == "get_random_verses":
            # parameters: count
            gitas = self.app.gita_repository.get_random_verses(parameters["count"])
            context = []

            for gita in gitas:
                context.append(
                    PatternMatchingContext(
                        label=f"BG {gita.c_chapter_number}.{gita.v_verse_number}",
                        content=f"{gita.v_text_sanskrit.strip()}\n\n{gita.vt_content.strip()}",
                        display_content=f"\n\n*{gita.v_text_sanskrit.strip()}*\n\n{gita.vt_content.strip()}",
                        link=f"{self.library_base_url}/chapter/{gita.c_chapter_number}/verse/{gita.v_verse_number}",
                    )
                )

            return PatternMatchingResult(type="context", context=context)
        elif action_type == "get_specific_verse":
            # parameters: chapter, verse
            gita = self.app.gita_repository.get_specific_verse(
                parameters["chapter"], parameters["verse"]
            )
            context = []

            if gita:
                context.append(
                    PatternMatchingContext(
                        label=f"BG {gita.c_chapter_number}.{gita.v_verse_number}",
                        content=f"""
Bab {gita.c_chapter_number} - {gita.c_name}\n
Ringkasan: {gita.c_summary}\n
Kode sloka: BG {gita.c_chapter_number}.{gita.v_verse_number}\n
Sanskerta: *{gita.v_text_sanskrit.strip()}*\n
Pengertian: {gita.vt_content.strip()}\n
                    """,
                        display_content=f"""
BG {gita.c_chapter_number}.{gita.v_verse_number}\n
*{gita.v_text_sanskrit.strip()}*\n
{gita.vt_content.strip()}\n
                        """,
                        attachments=[
                            Attachment(
                                type="url",
                                title=f"Bab {gita.c_chapter_number} Sloka {gita.v_verse_number}",
                                url=f"{self.library_base_url}/chapter/{gita.c_chapter_number}/verse/{gita.v_verse_number}",
                            ),
                            Attachment(
                                type="audio",
                                title=f"Audio sloka {gita.c_chapter_number}.{gita.v_verse_number}",
                                url=gita.v_audio_url,
                            ),
                        ],
                    )
                )

            return PatternMatchingResult(type="context", context=context)
        elif action_type == "get_sample_verses":
            # parameters: chapter, count, expandable
            gita_list = self.app.gita_repository.get_sample_verses(
                parameters["chapter"], parameters["count"]
            )
            context = []

            for gita in gita_list:
                context.append(
                    PatternMatchingContext(
                        label=f"BG {gita.c_chapter_number}.{gita.v_verse_number}",
                        content=f"\n\n*{gita.v_text_sanskrit.strip()}*\n\n{gita.vt_content.strip()}",
                        link=f"{self.library_base_url}/chapter/{gita.c_chapter_number}/verse/{gita.v_verse_number}",
                    )
                )

            return PatternMatchingResult(type="context", context=context)
        elif action_type == "get_chapter_summary":
            # parameters: chapter
            chapter = self.app.chapter_repository.get_chapter_by_number(
                parameters["chapter"]
            )
            print(f"{self.library_base_url}/chapter/20")
            context = []
            if chapter:
                context.append(
                    PatternMatchingContext(
                        label=f"BAB {chapter.chapter_number}",
                        content=f"""
Bab {chapter.chapter_number} - {chapter.name}\n
Ringkasan: {chapter.summary}\n
Jumlah ayat: {chapter.verses_count}\n
                    """,
                        display_content=f"""
Bab {chapter.chapter_number} - {chapter.name}\n
{chapter.summary}\n
                        """,
                        link=f"{self.library_base_url}/chapter/{chapter.chapter_number}",
                        attachments=[
                            Attachment(
                                type="url",
                                title=f"Bab {chapter.chapter_number} - {chapter.name}",
                                url=f"{self.library_base_url}/chapter/{chapter.chapter_number}",
                            ),
                        ],
                    )
                )

            return PatternMatchingResult(type="context", context=context)
        elif action_type == "get_chapter_metadata":
            # parameters: chapter, metadata_type
            chapter = self.app.chapter_repository.get_chapter_by_number(
                parameters["chapter"]
            )
            context = []
            if chapter:
                if parameters["metadata_type"] == "verse_count":
                    context.append(
                        PatternMatchingContext(
                            label=f"BAB {chapter.chapter_number}",
                            content=f"""
Bab {chapter.chapter_number} - {chapter.name}\n
Jumlah ayat: {chapter.verses_count}\n
                    """,
                            display_content=f"""
Bab {chapter.chapter_number} - {chapter.name}\n
Terdapat {chapter.verses_count} sloka di bab ini.\n
                            """,
                            link=f"{self.library_base_url}/chapter/{chapter.chapter_number}",
                            attachments=[
                                Attachment(
                                    type="url",
                                    title=f"Bab {chapter.chapter_number} - {chapter.name}",
                                    url=f"{self.library_base_url}/chapter/{chapter.chapter_number}",
                                ),
                            ],
                        )
                    )
                elif parameters["metadata_type"] == "chapter_name":
                    context.append(
                        PatternMatchingContext(
                            label=f"BAB {chapter.chapter_number}",
                            content=f"""
Bab {chapter.chapter_number} - {chapter.name}\n
                    """,
                            link=f"{self.library_base_url}/chapter/{chapter.chapter_number}",
                            attachments=[
                                Attachment(
                                    type="url",
                                    title=f"Bab {chapter.chapter_number} - {chapter.name}",
                                    url=f"{self.library_base_url}/chapter/{chapter.chapter_number}",
                                ),
                            ],
                        )
                    )

            return PatternMatchingResult(type="context", context=context)

        return None
