from repositories.report_repository import ReportRepository

class ReportController:
    def __init__(self):
        self.repository = ReportRepository()

    def obter_movimentacoes(self, tipo_relatorio, data_inicio, data_fim):
        return self.repository.relatorio_movimentacoes(tipo_relatorio, data_inicio, data_fim)

    def obter_produtos_estoque_baixo(self):
        return self.repository.listar_produtos_estoque_baixo()

    def obter_mais_movimentado_registro(self):
        return self.repository.mais_movimentados_registro()
    
    def obter_mais_movimentado_volume(self):
        return self.repository.mais_movimentados_volume()

    def obter_valor_total(self):
        return self. repository.valor_total_em_estoque()