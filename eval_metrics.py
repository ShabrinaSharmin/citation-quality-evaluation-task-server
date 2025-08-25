class EvaluationMetrics:
    def __init__(self, asqa=None, qampari=None, eli5=None):
        """
        Unified object for evaluation metrics across multiple datasets.

        Args:
            asqa (dict, optional): Dictionary with keys 'str_em', 'citation_rec', 'citation_prec'
            qampari (dict, optional): Dictionary with keys 'qampari_rec_top5', 'qampari_prec', 'citation_rec', 'citation_prec'
            eli5 (dict, optional): Dictionary with keys 'claims_nli', 'citation_prec', 'citation_rec'
        """
        self.asqa = asqa if asqa else {"str_em": 0.0, "citation_rec": 0.0, "citation_prec": 0.0}
        self.qampari = qampari if qampari else {"qampari_rec_top5": 0.0, "qampari_prec": 0.0,
                                                 "citation_rec": 0.0, "citation_prec": 0.0}
        self.eli5 = eli5 if eli5 else {"claims_nli": 0.0, "citation_prec": 0.0, "citation_rec": 0.0}

    def __repr__(self):
        return (f"EvaluationMetrics(\n"
                f"  ASQA={self.asqa},\n"
                f"  QAMPARI={self.qampari},\n"
                f"  ELI5={self.eli5}\n"
                f")")

    def to_dict(self):
        """
        Returns a dictionary representation of all metrics.
        """
        return {
            "ASQA": self.asqa,
            "QAMPARI": self.qampari,
            "ELI5": self.eli5
        }

    def update_asqa(self, str_em=None, citation_rec=None, citation_prec=None):
        if str_em is not None:
            self.asqa['str_em'] = str_em
        if citation_rec is not None:
            self.asqa['citation_rec'] = citation_rec
        if citation_prec is not None:
            self.asqa['citation_prec'] = citation_prec

    def update_qampari(self, qampari_rec_top5=None, qampari_prec=None, citation_rec=None, citation_prec=None):
        if qampari_rec_top5 is not None:
            self.qampari['qampari_rec_top5'] = qampari_rec_top5
        if qampari_prec is not None:
            self.qampari['qampari_prec'] = qampari_prec
        if citation_rec is not None:
            self.qampari['citation_rec'] = citation_rec
        if citation_prec is not None:
            self.qampari['citation_prec'] = citation_prec

    def update_eli5(self, claims_nli=None, citation_prec=None, citation_rec=None):
        if claims_nli is not None:
            self.eli5['claims_nli'] = claims_nli
        if citation_prec is not None:
            self.eli5['citation_prec'] = citation_prec
        if citation_rec is not None:
            self.eli5['citation_rec'] = citation_rec
