class QAMPARI:
    def __init__(self, qampari_rec_top5: float, qampari_prec: float, citation_rec: float, citation_prec: float):
        """
        Initialize a QAMPARI object.

        Args:
            qampari_rec_top5 (float): QAMPARI recall at top 5.
            qampari_prec (float): QAMPARI precision.
            citation_rec (float): Citation recall score.
            citation_prec (float): Citation precision score.
        """
        self.qampari_rec_top5 = qampari_rec_top5
        self.qampari_prec = qampari_prec
        self.citation_rec = citation_rec
        self.citation_prec = citation_prec

    def __repr__(self):
        return (f"QAMPARI(qampari_rec_top5={self.qampari_rec_top5}, "
                f"qampari_prec={self.qampari_prec}, "
                f"citation_rec={self.citation_rec}, "
                f"citation_prec={self.citation_prec})")

    def to_dict(self):
        """
        Return a dictionary representation of the QAMPARI object.
        """
        return {
            "Correctness Req.-5": self.qampari_rec_top5,
            "Correctness Prec": self.qampari_prec,
            "Citation Rec": self.citation_rec,
            "Citation Prec": self.citation_prec
        }
