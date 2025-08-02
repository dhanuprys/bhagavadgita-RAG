import yaml
import requests
import time

def query_rag_api(question: str) -> dict:
    """
    Fungsi ini memanggil web API RAG Anda untuk mendapatkan jawaban dan konteks.
    """
    API_URL = "https://gita-api.dedan.my.id/prompt"
    payload = {"message": question}
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        generated_answer = data.get("answer", "Error: Kunci 'answer' tidak ditemukan.")
        retrieved_contexts = [ctx.get("content", "") for ctx in data.get("context", [])]
        return {"answer": generated_answer, "contexts": retrieved_contexts}
    except requests.exceptions.RequestException as e:
        print(f"Error saat memanggil API untuk pertanyaan '{question}': {e}")
        return {"answer": "Gagal terhubung ke API RAG.", "contexts": []}

def main():
    """
    Membaca file QnA, memanggil API untuk setiap pertanyaan, dan menyimpan hasilnya.
    """
    input_filename = 'gita_test_set_final.yml'
    output_filename = 'rag_results.yml'

    print(f"Memuat file QnA dari '{input_filename}'...")
    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            qna_data = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' tidak ditemukan.")
        return

    all_results = []
    total_questions = len(qna_data)

    print(f"\nMengumpulkan jawaban dari API RAG untuk {total_questions} pertanyaan...")
    for i, item in enumerate(qna_data):
        question = item['question']
        ground_truth = item['answer']
        
        print(f"  Mengirim pertanyaan {i+1}/{total_questions}: \"{question[:50]}...\"")
        api_output = query_rag_api(question)
        
        # Gabungkan semua data menjadi satu dictionary
        result_entry = {
            'question': question,
            'answer': api_output['answer'],
            'contexts': api_output['contexts'],
            'ground_truth': ground_truth
        }
        all_results.append(result_entry)
        
        # Tambahkan jeda 1 detik
        time.sleep(1)

    print("\nPengumpulan hasil dari API selesai.")

    # Simpan semua hasil ke file YAML baru
    with open(output_filename, 'w', encoding='utf-8') as file:
        yaml.dump(all_results, file, allow_unicode=True, sort_keys=False)
        
    print(f"Hasil telah berhasil disimpan ke file '{output_filename}'")

if __name__ == "__main__":
    main()