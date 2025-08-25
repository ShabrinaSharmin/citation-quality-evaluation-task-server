class ASQA:
    def __init__(self, str_em: float, citation_rec: float, citation_prec: float):
        """
        Initialize an ASQA object.

        Args:
            str_em (float): String-level exact match score.
            citation_rec (float): Citation recall score.
            citation_prec (float): Citation precision score.
        """
        self.str_em = str_em
        self.citation_rec = citation_rec
        self.citation_prec = citation_prec

    def __repr__(self):
        return (f"ASQA(str_em={self.str_em}, "
                f"citation_rec={self.citation_rec}, "
                f"citation_prec={self.citation_prec})")

    def to_dict(self):
        """
        Return a dictionary representation of the ASQA object.
        """
        return {
            "Correctness EM_REC": self.str_em,
            "Citation Rec": self.citation_rec,
            "Citation Prec": self.citation_prec
        }
