import json, os
from eval_metrics import EvaluationMetrics
from eli5 import ELI5
from asqa import ASQA
from qampari import QAMPARI
PREFIX = "./results/"
def open_and_print(email: str, n1: int, n2: int, n3:int):
    filenames = [f"{email}_task_{n1}.json", f"{email}_task_{n2}.json", f"{email}_task_{n3}.json"]
    
    for file in filenames:
        file_path = os.path.join(PREFIX, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"\nContents of {file}:")
                print("ASQA")
                print(data["ASQA"]["str_em"])
                print(data["ASQA"]["citation_rec"])
                print(data["ASQA"]["citation_prec"])

                if "ELI5" in data:
                    print("ELI5")
                    print(data["ELI5"]["claims_nli"])
                    print(data["ELI5"]["citation_rec"])
                    print(data["ELI5"]["citation_prec"])

                
                if "QAMPARI" in data:
                    print("QAMPARI")
                    print(data["QAMPARI"]["qampari_rec_top5"])
                    print(data["QAMPARI"]["qampari_prec"])
                    print(data["QAMPARI"]["citation_rec"])
                    print(data["QAMPARI"]["citation_prec"])
                print("Doneeee!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        except FileNotFoundError:
            print(f"File not found: {file}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in: {file}")

# Example usage
if __name__ == '__main__':
    open_and_print("alice@cqets.com", 1, 2, 3)
    metrics = EvaluationMetrics()

    # Update ASQA scores
    metrics.update_asqa(str_em=0.75, citation_rec=0.82, citation_prec=0.85)

    # Update QAMPARI scores
    metrics.update_qampari(qampari_rec_top5=0.78, qampari_prec=0.80, citation_rec=0.83, citation_prec=0.87)

    # Update ELI5 scores
    metrics.update_eli5(claims_nli=0.81, citation_prec=0.84, citation_rec=0.88)

    # Print the object
    print(metrics)


    # Convert to dictionary
    metrics_dict = metrics.to_dict()
    print(metrics_dict)