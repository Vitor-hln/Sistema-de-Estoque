from database import conectar

class ReportRepository:
    def listar_relatorios(self, tipo_relatorio, data_inicio, data_fim):
        """Busca os dados reais do banco para os relatórios"""
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        try:
            query ="""
                SELECT 
                m.tipo, 
                m.quantidade, 
                m.usuario, 
                p.nome AS produto, 
                m.data_hora,
                GREATEST(
                    0,  -- Se `qtd_atualizada` for menor que 0, exibe 0
                    (
                        SELECT COALESCE(SUM(
                            CASE 
                                WHEN m2.tipo = 'Entrada' THEN m2.quantidade 
                                ELSE -m2.quantidade 
                            END
                        ), 0)
                        FROM movimentacoes m2
                        WHERE m2.produto_id = m.produto_id 
                        AND m2.data_hora <= m.data_hora
                    )
                ) AS qtd_atualizada
            FROM movimentacoes m
            JOIN produtos p ON m.produto_id = p.id
            WHERE m.data_hora BETWEEN %s AND %s
            """
            
            parametros = [data_inicio, data_fim]

            # Adicionar filtro pelo tipo de relatório
            if tipo_relatorio == "Movimentações de Estoque":
                pass  # Sem filtro adicional
            elif tipo_relatorio == "Produtos com Estoque Baixo":
                query += " AND p.quantidade < p.estoque_minimo"
            elif tipo_relatorio == "Produtos Mais Movimentados":
                query += " ORDER BY m.quantidade DESC"
            elif tipo_relatorio == "Valor Total em Estoque":
                query = """
                    SELECT 
                        p.id, p.nome AS produto, p.quantidade, p.valor_unitario,
                        (p.quantidade * p.valor_unitario) AS valor_total
                    FROM produtos p
                """

            cursor.execute(query, parametros)
            return cursor.fetchall()

        except Exception as e:
            print(f"Erro ao buscar relatórios: {e}")
            return []
        finally:
            cursor.close()
            conexao.close()


    def listar_produtos_estoque_baixo(self):
        """Busca os produtos com estoque baixo"""
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    p.nome AS produto,
                    p.quantidade AS estoque_atual,
                    p.estoque_minimo,
                    CASE 
                        WHEN p.quantidade <= p.estoque_minimo * 0.5 THEN 'CRÍTICO'
                        WHEN p.quantidade <= p.estoque_minimo THEN 'BAIXO'
                        ELSE 'NORMAL'
                    END AS status
                FROM produtos p
                WHERE p.quantidade <= p.estoque_minimo
                ORDER BY 
                    CASE 
                        WHEN p.quantidade <= p.estoque_minimo * 0.5 THEN 1
                        WHEN p.quantidade <= p.estoque_minimo THEN 2
                        ELSE 3
                    END,
                    p.nome
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar produtos com estoque baixo: {e}")
            return []
        finally:
            cursor.close()
            conexao.close()
