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
# CONFIGURAÇÃO
# ============================================================

ENTAILMENT_THRESHOLD = 0.45


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


    # ========================================================
    # PREDIÇÃO NLI
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


    # ========================================================
    # SEPARAÇÃO DAS CLAIMS
    # ========================================================

    @staticmethod
    def split_claims(answer: str):

        claims = []

        sentences = answer.replace("!", ".").replace("?", ".").split(".")

        for sentence in sentences:

            claim = sentence.strip()

            if claim:
                claims.append(claim)

        return claims


    # ========================================================
    # AVALIAÇÃO DE FAITHFULNESS
    # ========================================================

    def evaluate(
        self,
        context: str,
        generated_answer: str,
    ):

        claims = self.split_claims(
            generated_answer
        )

        if not claims:
            return {
                "faithfulness_score": 0.0,
                "total_claims": 0,
                "supported_claims": 0,
                "claims": [],
            }

        results = []

        supported_claims = 0

        for index, claim in enumerate(claims, start=1):

            result = self.predict(
                context=context,
                claim=claim,
            )

            is_supported = (
                result["label"] == "entailment"
                and result["entailment"] >= ENTAILMENT_THRESHOLD
            )

            if is_supported:
                supported_claims += 1

            results.append({
                "claim_id": index,
                "claim": claim,
                "label": result["label"],
                "entailment": result["entailment"],
                "neutral": result["neutral"],
                "contradiction": result["contradiction"],
                "supported": is_supported,
            })

        faithfulness_score = (
            supported_claims / len(claims)
        )

        return {
            "faithfulness_score": faithfulness_score,
            "total_claims": len(claims),
            "supported_claims": supported_claims,
            "claims": results,
        }


# ============================================================
# TESTE DE FAITHFULNESS
# ============================================================

def main():

    print("=" * 60)
    print("AVALIAÇÃO DE FAITHFULNESS - SUSE AI ASSISTANT")
    print("=" * 60)
    print()

    evaluator = FaithfulnessEvaluator()

    # --------------------------------------------------------
    # CONTEXTO RECUPERADO PELO RAG
    # --------------------------------------------------------

    context = (
        "Uma OS pode ser aprovada pelo cliente. "
        "Após a aprovação, a OS pode ser agendada "
        "para execução do serviço."
    )

    # --------------------------------------------------------
    # RESPOSTA GERADA PELO RAG
    # --------------------------------------------------------

    generated_answer = (
        "A OS pode ser aprovada pelo cliente. "
        "Após a aprovação, a OS pode ser agendada "
        "para execução do serviço. "
        "O cliente recebe automaticamente uma mensagem "
        "pelo WhatsApp."
    )

    print("CONTEXTO:")
    print(context)

    print("\nRESPOSTA GERADA:")
    print(generated_answer)

    print("\nExecutando avaliação...\n")

    result = evaluator.evaluate(
        context=context,
        generated_answer=generated_answer,
    )

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    print("=" * 60)
    print("RESULTADO")
    print("=" * 60)

    print(
        f"\nFaithfulness Score: "
        f"{result['faithfulness_score']:.2%}"
    )

    print(
        f"Claims suportadas: "
        f"{result['supported_claims']}/"
        f"{result['total_claims']}"
    )

    print("\nANÁLISE DAS CLAIMS:")
    print("-" * 60)

    for claim_result in result["claims"]:

        print(
            f"\nClaim {claim_result['claim_id']}:"
        )

        print(
            f"  {claim_result['claim']}"
        )

        print(
            f"  Classificação: "
            f"{claim_result['label']}"
        )

        print(
            f"  Entailment: "
            f"{claim_result['entailment']:.4f}"
        )

        print(
            f"  Neutral: "
            f"{claim_result['neutral']:.4f}"
        )

        print(
            f"  Contradiction: "
            f"{claim_result['contradiction']:.4f}"
        )

        print(
            f"  Suportada: "
            f"{'SIM' if claim_result['supported'] else 'NÃO'}"
        )

    print("\n" + "=" * 60)


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()

