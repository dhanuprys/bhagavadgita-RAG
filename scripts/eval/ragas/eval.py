import os
import yaml
import time
from langchain_google_genai import ChatGoogleGenerativeAI, _genai_extension as genaix
from typing import Any, List, Optional, Union, Sequence, Dict, Callable
from langchain_core.messages import (
    BaseMessage,
)
from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForLLMRun
)
from google.ai.generativelanguage_v1beta.types import Tool as GoogleTool
from langchain_google_genai._function_utils import (
    _ToolChoiceType,
    _ToolConfigDict,
    _ToolDict,
)
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
    answer_correctness,
)
from google.ai.generativelanguage_v1beta.types import (
    FunctionDeclaration,
    GenerateContentResponse,
)
import asyncio
from google.ai.generativelanguage_v1beta import (
    GenerativeServiceAsyncClient as v1betaGenerativeServiceAsyncClient,
)
from langchain_core.outputs import ChatResult
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai._common import (
    SafetySettingDict,
    get_client_info,
)

# ===============================================================
# PERSIAPAN MODEL EVALUATOR (GEMINI)
# ===============================================================

# Atur Google AI API Key Anda
os.environ["GOOGLE_API_KEY"] = "AIzaSyDgPpmtEWPUWRi8kPWh2Ae1EIJ3oIJVvW8"
GEMINI_API_KEYS=["AIzaSyBgeoSSElNpNt9UDQ3yziqfOX9MjznLGxU", "AIzaSyBEYbpq5uRFHJKnMV4E5ZC2LZKXcsr2AHA", "AIzaSyCpBuj11SnLaRr2xdsV0eRFpvnwREiRT_M", "AIzaSyASPfDNLVKq6g1dmZfoUkLxoNGd_FzmXso", "AIzaSyCZcjNsf-Fpw5EmZYoZYW_dSNOLQj_zeCU", "AIzaSyDGkLAbahF9kJpzfmp6eVevECYQlTDJj-k", "AIzaSyClYRz4JyqGmhrF_VFbOHd6rgx5SwwCZtE", "AIzaSyCixE3zYvXWa4P52NxnJViLOoW7k3iy7KQ", "AIzaSyCmn9Q2fitfMaMwaRkfAICNQPd40m7EHxk", "AIzaSyBgNZLMBqMGA6tcspviFqfHDbUvcX9WMXk", "AIzaSyCozswOipLBUxT2rUlRrMVvgAgrTmEZaOg", "AIzaSyBofWXDgi7HkDKYXYHQadsZKP3gAiOwD6E", "AIzaSyAQ3bhzKP3sMrGr_SNk_U4QGJcYR6XUG5w", "AIzaSyA4POABII3n7QK41JWh9nv3vw3xjdVr-hc", "AIzaSyD08ivtHkc9JsKFPomiueRpytjBw6s-UI4", "AIzaSyBzmnYrbaU7jJNM8wvTH9guAaM-mWvgoAs", "AIzaSyDgPpmtEWPUWRi8kPWh2Ae1EIJ3oIJVvW8", "AIzaSyDUBWwS9hrsOVxM974RdUeDpsYRRujqi4A", "AIzaSyB2TuW6LTCpg4A7xLppNkuc0m9fFWKabMQ", "AIzaSyAuleTc6_oas-FsrtMlueLW9AVdXbJ1zkE"]

_FunctionDeclarationType = Union[
    FunctionDeclaration,
    dict[str, Any],
    Callable[..., Any],
]

def _is_event_loop_running() -> bool:
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False

class RateLimitedChatGoogleGenerativeAI(ChatGoogleGenerativeAI):
    delay_seconds: float = 5
    key_index: int = 0
    max_key_index: int = len(GEMINI_API_KEYS) - 1

    @property
    def async_client(self) -> v1betaGenerativeServiceAsyncClient:
        google_api_key = GEMINI_API_KEYS[self.key_index]
        print(f"Using {self.key_index}>>>{google_api_key}")

        # if self.key_index != self.max_key_index:
        #     self.key_index += 1
        # else:
        #     self.key_index = 0

        with open('./current_key', 'w') as f:
            f.write(google_api_key)

        # NOTE: genaix.build_generative_async_service requires
        # a running event loop, which causes an error
        # when initialized inside a ThreadPoolExecutor.
        # this check ensures that async client is only initialized
        # within an asyncio event loop to avoid the error
        if not self.async_client_running and _is_event_loop_running():
            # async clients don't support "rest" transport
            # https://github.com/googleapis/gapic-generator-python/issues/1962
            transport = self.transport
            if transport == "rest":
                transport = "grpc_asyncio"
            self.async_client_running = genaix.build_generative_async_service(
                credentials=self.credentials,
                api_key=google_api_key,
                client_info=get_client_info(f"ChatGoogleGenerativeAI:{self.model}"),
                client_options=self.client_options,
                transport=transport,
            )
        return self.async_client_running

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        *,
        tools: Optional[Sequence[Union[_ToolDict, GoogleTool]]] = None,
        functions: Optional[Sequence[_FunctionDeclarationType]] = None,
        safety_settings: Optional[SafetySettingDict] = None,
        tool_config: Optional[Union[Dict, _ToolConfigDict]] = None,
        generation_config: Optional[Dict[str, Any]] = None,
        cached_content: Optional[str] = None,
        tool_choice: Optional[Union[_ToolChoiceType, bool]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        print(f"Waiting for {self.delay_seconds} seconds")
        time.sleep(self.delay_seconds)
        return await super()._agenerate(
            messages,
            stop,
            run_manager,
            tools=tools,
            functions=functions,
            safetry_settings=safety_settings,
            tool_config=tool_config,
            generation_config=generation_config,
            cached_content=cached_content,
            tool_choice=tool_choice,
            **kwargs
        )

print("Menginisialisasi model evaluator (Gemini & HuggingFace)...")
evaluator_llm = RateLimitedChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")
evaluator_embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
print("Model evaluator siap.")

# ===============================================================
# PROSES EVALUASI
# ===============================================================

def main():
    input_filename = 'rag_results.yml'

    print(f"\nMemuat hasil RAG dari file '{input_filename}'...")
    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            results_data = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' tidak ditemukan. Jalankan skrip 'collect_results.py' terlebih dahulu.")
        return

    print("Menyiapkan dataset untuk evaluasi...")
    
    # Membuat dictionary untuk dataset dengan format yang benar
    dataset_dict = {
        'question': [item.get('question', '') for item in results_data],
        'answer': [item.get('answer', '') for item in results_data],
        'contexts': [item.get('contexts', []) for item in results_data],
        # === PERBAIKAN DI SINI ===
        # 'ground_truth' harus berupa list of strings, bukan list of lists
        'ground_truth': [item.get('ground_truth', '') for item in results_data]
    }
        
    dataset = Dataset.from_dict(dataset_dict)

    # Definisikan metrik
    metrics_to_use = [
        faithfulness,
        answer_relevancy,
        context_recall,
        context_precision,
        answer_correctness,
    ]
    
    print("\nMemulai evaluasi dengan Ragas menggunakan Gemini. Proses ini mungkin memakan waktu...")
    result = evaluate(
        dataset=dataset,
        metrics=metrics_to_use,
        llm=evaluator_llm,
        embeddings=evaluator_embeddings
    )
    print("Evaluasi selesai!")

    # Tampilkan dan simpan hasil
    df_results = result.to_pandas()
    print("\n--- HASIL EVALUASI RAGAS (DENGAN GEMINI) ---")
    print(df_results.to_string())
    print("---------------------------------------------")

    df_results.to_csv("ragas_evaluation_final_results.csv", index=False)
    print("\nHasil evaluasi telah disimpan ke file 'ragas_evaluation_final_results.csv'")

if __name__ == "__main__":
    main()