from pathlib import Path

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer


# ============================================================
# CAMINHOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "models" / "grounding"

MODEL_PATH = MODEL_DIR / "model_quantized.onnx"
TOKENIZER_PATH = MODEL_DIR / "tokenizer.json"


# ============================================================
# LABELS DO MODELO
# ============================================================

LABELS = {
    0: "entailment",
    1: "neutral",
    2: "contradiction",
}


# ============================================================
# AVALIADOR
# ============================================================

class FaithfulnessEvaluator:

    def __init__(self):

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Modelo não encontrado:\n{MODEL_PATH}"
            )

        if not TOKENIZER_PATH.exists():
            raise FileNotFoundError(
                f"Tokenizer não encontrado:\n{TOKENIZER_PATH}"
            )

        print("Carregando tokenizer...")

        self.tokenizer = Tokenizer.from_file(
            str(TOKENIZER_PATH)
        )

        print("Carregando modelo ONNX...")

        self.session = ort.InferenceSession(
            str(MODEL_PATH),
            providers=["CPUExecutionProvider"],
        )

        print("Modelo carregado com sucesso.\n")

        print("Inputs do modelo:")

        for input_info in self.session.get_inputs():
            print(
                f"  - {input_info.name}: "
                f"{input_info.shape} "
                f"{input_info.type}"
            )

        print("\nOutputs do modelo:")

        for output_info in self.session.get_outputs():
            print(
                f"  - {output_info.name}: "
                f"{output_info.shape} "
                f"{output_info.type}"
            )

        print()

    # ========================================================
    # PREDIÇÃO
    # ========================================================

    def predict(self, context: str, claim: str):

        encoding = self.tokenizer.encode(
            context,
            claim,
        )

        input_ids = np.array(
            [encoding.ids],
            dtype=np.int64,
        )

        attention_mask = np.array(
            [encoding.attention_mask],
            dtype=np.int64,
        )

        inputs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
        }

        outputs = self.session.run(
            None,
            inputs,
        )

        logits = outputs[0][0]

        probabilities = self.softmax(logits)

        label_id = int(
            np.argmax(probabilities)
        )

        label = LABELS[label_id]

        return {
            "label": label,
            "entailment": float(probabilities[0]),
            "neutral": float(probabilities[1]),
            "contradiction": float(probabilities[2]),
        }

    # ========================================================
    # SOFTMAX
    # ========================================================

    @staticmethod
    def softmax(logits):

        logits = logits - np.max(logits)

        probabilities = np.exp(logits)

        return probabilities / probabilities.sum()


# ============================================================
# TESTE
# ============================================================

def main():

    print("=" * 60)
    print("TESTE DO MODELO NLI - SUSE AI ASSISTANT")
    print("=" * 60)
    print()

    evaluator = FaithfulnessEvaluator()

    context = (
        "Quando uma OS é marcada como FINALIZADO, "
        "o sistema registra o histórico do cliente."
    )

    claim = (
        "Quando a OS é finalizada, "
        "o sistema registra o histórico do cliente."
    )

    print("CONTEXTO:")
    print(context)

    print("\nAFIRMAÇÃO:")
    print(claim)

    print("\nExecutando NLI...\n")

    result = evaluator.predict(
        context=context,
        claim=claim,
    )

    print("RESULTADO:")
    print(f"Classificação: {result['label']}")
    print(
        f"Entailment:   {result['entailment']:.4f}"
    )
    print(
        f"Neutral:       {result['neutral']:.4f}"
    )
    print(
        f"Contradiction: {result['contradiction']:.4f}"
    )

    print("\n" + "=" * 60)


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()

