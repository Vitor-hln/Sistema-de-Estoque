from repositories.report_repository import ReportRepository

class ReportController:
    def __init__(self):
        self.repository = ReportRepository()

    def obter_relatorios(self, tipo_relatorio, data_inicio, data_fim):
        return self.repository.listar_relatorios(tipo_relatorio, data_inicio, data_fim)
