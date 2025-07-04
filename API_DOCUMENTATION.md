# Bhagavad Gita API Documentation

This API provides access to the complete Bhagavad Gita text, including all 18 chapters, 700+ verses, translations, and AI-powered chat functionality.

## Base URL
```
http://localhost:8000
```

## API Endpoints

### Chapters

#### GET /chapter
Get all chapters of the Bhagavad Gita.

**Response:** `List[ChapterResponse]`

**Example Response:**
```json
[
  {
    "id": 1,
    "chapter_number": 1,
    "name": "Dilema Arjuna",
    "name_hindi": "अर्जुनविषादयोग",
    "name_sanskrit": "Arjun Viṣhād Yog",
    "summary": "Bab pertama Bhagavad Gita - \"Arjuna Vishada Yoga\" memperkenalkan latar belakang, pengaturan, karakter, dan keadaan yang menyebabkan pertempuran epik Mahabharata, yang diperjuangkan antara Pandawa dan Kurawa. Bab ini menguraikan alasan-alasan yang menyebabkan terungkapnya Bhagavad Gita.\nSaat kedua pasukan berdiri siap untuk pertempuran, prajurit perkasa Arjuna, saat mengamati para prajurit di kedua belah pihak, menjadi semakin sedih dan tertekan karena ketakutan kehilangan kerabat dan teman-temannya serta dosa-dosa yang diakibatkan oleh pembunuhan kerabatnya sendiri. Maka, ia menyerah kepada Dewa Krishna, mencari solusi. Demikianlah, muncullah kebijaksanaan Bhagavad Gita.",
    "verses_count": 47
  }
]
```

#### GET /chapter/{chapter_number}
Get a specific chapter by its number (1-18).

**Parameters:**
- `chapter_number` (int): Chapter number (1-18)

**Response:** `ChapterResponse`

**Example Response:**
```json
{
  "id": 1,
  "chapter_number": 1,
  "name": "Dilema Arjuna",
  "name_hindi": "अर्जुनविषादयोग",
  "name_sanskrit": "Arjun Viṣhād Yog",
  "summary": "Bab pertama Bhagavad Gita - \"Arjuna Vishada Yoga\" memperkenalkan latar belakang, pengaturan, karakter, dan keadaan yang menyebabkan pertempuran epik Mahabharata, yang diperjuangkan antara Pandawa dan Kurawa. Bab ini menguraikan alasan-alasan yang menyebabkan terungkapnya Bhagavad Gita.\nSaat kedua pasukan berdiri siap untuk pertempuran, prajurit perkasa Arjuna, saat mengamati para prajurit di kedua belah pihak, menjadi semakin sedih dan tertekan karena ketakutan kehilangan kerabat dan teman-temannya serta dosa-dosa yang diakibatkan oleh pembunuhan kerabatnya sendiri. Maka, ia menyerah kepada Dewa Krishna, mencari solusi. Demikianlah, muncullah kebijaksanaan Bhagavad Gita.",
  "verses_count": 47
}
```

**Error Response (404):**
```json
{
  "detail": "Item not found"
}
```

### Verses

#### GET /chapter/{chapter_number}/verse
Get all verses from a specific chapter.

**Parameters:**
- `chapter_number` (int): Chapter number (1-18)

**Response:** `List[VerseResponse]`

**Example Response:**
```json
[
  {
    "id": 1,
    "verse_number": 1,
    "text_hindi": "धृतराष्ट्र उवाच\n\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।\n\nमामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय।।1.1।।\n",
    "text_sanskrit": "dhṛitarāśhtra uvācha\ndharma-kṣhetre kuru-kṣhetre samavetā yuyutsavaḥ\nmāmakāḥ pāṇḍavāśhchaiva kimakurvata sañjaya\n",
    "text_sanskrit_meanings": "dhṛitarāśhtraḥ uvācha—Dhritarashtra said; dharma-kṣhetre—the land of dharma; kuru-kṣhetre—at Kurukshetra; samavetāḥ—having gathered; yuyutsavaḥ—desiring to fight; māmakāḥ—my sons; pāṇḍavāḥ—the sons of Pandu; cha—and; eva—certainly; kim—what; akurvata—did they do; sañjaya—Sanjay\n",
    "audio_url": "https://gita.github.io/gita/data/verse_recitation/1/1.mp3",
    "chapter_id": 1
  }
]
```

#### GET /chapter/{chapter_number}/verse/{verse_number}
Get a specific verse with all its translations.

**Parameters:**
- `chapter_number` (int): Chapter number (1-18)
- `verse_number` (int): Verse number within the chapter

**Response:** `VerseDetailResponse`

**Example Response:**
```json
{
  "id": 1,
  "verse_number": 1,
  "text_hindi": "धृतराष्ट्र उवाच\n\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।\n\nमामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय।।1.1।।\n",
  "text_sanskrit": "dhṛitarāśhtra uvācha\ndharma-kṣhetre kuru-kṣhetre samavetā yuyutsavaḥ\nmāmakāḥ pāṇḍavāśhchaiva kimakurvata sañjaya\n",
  "text_sanskrit_meanings": "dhṛitarāśhtraḥ uvācha—Dhritarashtra said; dharma-kṣhetre—the land of dharma; kuru-kṣhetre—at Kurukshetra; samavetāḥ—having gathered; yuyutsavaḥ—desiring to fight; māmakāḥ—my sons; pāṇḍavāḥ—the sons of Pandu; cha—and; eva—certainly; kim—what; akurvata—did they do; sañjaya—Sanjay\n",
  "audio_url": "https://gita.github.io/gita/data/verse_recitation/1/1.mp3",
  "chapter_id": 1,
  "translations": [
    {
      "id": 1,
      "content": "Dhṛtarāṣṭra berkata: \"Wahai Sanjaya, apa yang dilakukan rakyatku dan para Pandawa, yang berkumpul di medan suci Kurukshetra, bersemangat untuk bertempur?\"",
      "verse_id": 1
    },
    {
      "id": 2,
      "content": "Dhritarashtra bertanya: \"Wahai Sanjaya, apa yang terjadi saat putra-putraku dan putra-putra Pandu berkumpul di tanah suci Kurukshetra, penuh gairah untuk bertempur?\"",
      "verse_id": 1
    }
  ]
}
```

**Error Response (404):**
```json
{
  "detail": "Item not found"
}
```

### AI Chat

#### POST /prompt
Ask AI about Bhagavad Gita and get an intelligent response with context.

**Request Body:** `PromptRequest`
```json
{
  "message": "Tolong berikan isi dari Bhagavad Gita bab 2 sloka 47"
}
```

**Response:** `PromptResponse`

**Example Response:**
```json
{
  "answer": "Tentu, dengan senang hati saya akan memberikan penjelasan mengenai Bhagavad Gita bab 2, sloka 47:\n\n> *karmaṇy-evādhikāras te mā phaleṣhu kadāchana\nmā karma-phala-hetur bhūr mā te saṅgo 'stvakarmaṇi*\n\nMaknanya adalah:\n\n> Engkau hanya memiliki hak untuk bekerja, tetapi tidak untuk buahnya. Jangan terdorong oleh hasil kerjamu, pun jangan terikat pada kelambanan.\n\nSloka ini mengajarkan kita untuk fokus pada pelaksanaan tugas dengan sebaik-baiknya tanpa terpaku pada hasil yang akan didapatkan. Kita hendaknya tidak termotivasi semata-mata oleh imbalan atau takut akan kegagalan, dan juga tidak boleh menjadi malas atau menghindari tindakan.\n",
  "context": [
    {
      "label": "BG 2.47",
      "content": "\nBG 2.47\n\n*karmaṇy-evādhikāras te mā phaleṣhu kadāchana\nmā karma-phala-hetur bhūr mā te saṅgo 'stvakarmaṇi*\n\nEngkau hanya memiliki hak untuk bekerja, tetapi tidak untuk buahnya. Jangan terdorong oleh hasil kerjamu, pun jangan terikat pada kelambanan.\n",
      "link": null
    }
  ],
  "answer_system": "intent",
  "suggestions": [
    "ceritakan tentang bab 2",
    "Bab 7 itu intinya tentang apa?",
    "Tolong berikan isi dari Bhagavad Gita bab 2 sloka 47.",
    "tunjukkan isi dari bab 6"
  ],
  "attachments": []
}
```

**Response Fields:**
- `answer` (str): AI-generated response to the user's question
- `context` (List[ChatContextResponse]): Relevant verses or chapters used as context
- `answer_system` (str): Either "intent" (pattern-matched) or "semantic" (AI search)
- `suggestions` (List[str]): 4 random question suggestions for follow-up
- `attachments` (List[AttachmentResponse]): Related audio files or links

#### GET /suggestions
Get random question suggestions for users.

**Response:** `SuggestionsResponse`

**Example Response:**
```json
{
  "suggestions": [
    "ceritakan tentang bab 2",
    "Bab 7 itu intinya tentang apa?",
    "Tolong berikan isi dari Bhagavad Gita bab 2 sloka 47.",
    "tunjukkan isi dari bab 6"
  ]
}
```

## Data Models

### ChapterResponse
```typescript
{
  id: number
  chapter_number: number
  name: string
  name_hindi: string
  name_sanskrit: string
  summary: string
  verses_count: number
}
```

### VerseResponse
```typescript
{
  id: number
  verse_number: number
  text_hindi: string
  text_sanskrit: string
  text_sanskrit_meanings: string
  audio_url: string
  chapter_id: number
}
```

### VerseDetailResponse
```typescript
{
  id: number
  verse_number: number
  text_hindi: string
  text_sanskrit: string
  text_sanskrit_meanings: string
  audio_url: string
  chapter_id: number
  translations: VerseTranslationResponse[]
}
```

### VerseTranslationResponse
```typescript
{
  id: number
  content: string
  verse_id: number
}
```

### PromptRequest
```typescript
{
  message: string
}
```

### PromptResponse
```typescript
{
  answer: string
  context: ChatContextResponse[]
  answer_system: "intent" | "semantic"
  suggestions: string[]
  attachments: AttachmentResponse[]
}
```

### ChatContextResponse
```typescript
{
  label: string
  content: string
  link: string | null
}
```

### AttachmentResponse
```typescript
{
  type: "audio" | "url"
  title: string
  url: string
  description: string
}
```

### SuggestionsResponse
```typescript
{
  suggestions: string[]
}
```

### ErrorResponse
```typescript
{
  detail: string
}
```

## Error Codes

- `400`: Bad Request - Invalid request format
- `404`: Not Found - Requested resource not found

## Features

### AI Chat Capabilities
The AI chat system can handle various types of questions:

1. **Specific Verse Requests**: "Tolong berikan isi dari Bhagavad Gita bab 2 sloka 47"
2. **Chapter Summaries**: "ceritakan tentang bab 2"
3. **Random Verses**: "berikan saya satu sloka acak"
4. **Metadata Queries**: "ada berapa total sloka di bab 15?"
5. **Semantic Search**: General questions about Bhagavad Gita concepts

### Multilingual Support
- Sanskrit text with transliteration
- Hindi text
- Indonesian translations
- English translations

### Audio Support
- Verse recitation audio files available
- Audio URLs provided in verse responses

### Smart Suggestions
- Context-aware question suggestions
- Random suggestions for user engagement

## Usage Examples

### Get Chapter Information
```bash
curl -X GET "http://localhost:8000/chapter/1"
```

### Get Verse with Translations
```bash
curl -X GET "http://localhost:8000/chapter/1/verse/1"
```

### Ask AI About Bhagavad Gita
```bash
curl -X POST "http://localhost:8000/prompt" \
  -H "Content-Type: application/json" \
  -d '{"message": "Tolong berikan isi dari Bhagavad Gita bab 2 sloka 47"}'
```

### Get Question Suggestions
```bash
curl -X GET "http://localhost:8000/suggestions"
```

## Swagger Documentation

The API includes comprehensive Swagger/OpenAPI documentation available at:
```
http://localhost:8000/docs
```

This provides an interactive API explorer with:
- All endpoint descriptions
- Request/response schemas
- Example requests and responses
- Try-it-out functionality 