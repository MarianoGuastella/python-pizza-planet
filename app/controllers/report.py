from app.repositories.reports.report import ReportStrategy


class ReportController:
    def __init__(self, strategy: ReportStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ReportStrategy):
        self._strategy = strategy

    def generate_report(self):
        return self._strategy.generate()
