# Requisitos - Sistema Autônomo de Gestão de Pedidos para Hamburgueria

## 1. Objetivo
Sistema que gerencia pedidos, estoque e comunicação com a cozinha de uma hamburgueria, reduzindo erros manuais e agilizando o atendimento.

## 2. Atores
- Cliente
- Atendente
- Cozinha
- Gerente

## 3. Requisitos funcionais (escopo mínimo)
- RF01: O sistema deve cadastrar, editar e excluir produtos do cardápio.
- RF02: O sistema deve cadastrar insumos com seus respectivos estoques mínimos.
- RF03: O sistema deve registrar pedidos via interface web.
- RF04: O sistema deve verificar automaticamente a disponibilidade de cada item no estoque ao registrar um pedido.
- RF05: O sistema deve descontar os insumos do estoque ao confirmar um pedido.
- RF06: O sistema deve enviar o pedido confirmado para a fila da cozinha (painel/tela).
- RF07: O sistema deve notificar o atendente quando um item estiver indisponível, permitindo substituição.
- RF08: O sistema deve emitir alerta quando um insumo ficar abaixo do estoque mínimo.
- RF09: O sistema deve gerar relatório diário de vendas e produtos mais pedidos.
- RF10: O sistema deve enviar o relatório diário em PDF por e-mail ao gerente ao final do expediente.

## 4. Requisitos não funcionais
- RNF01: API própria em Python (Flask).
- RNF02: Banco PostgreSQL com migrations versionadas.
- RNF03: Aplicação e banco orquestrados com Docker Compose.
- RNF04: Segredos fora do código (variáveis de ambiente via python-dotenv).
- RNF05: Geração de relatórios em PDF (fpdf2).
- RNF06: Envio de e-mails via smtplib.

## 5. Mensagens que o sistema envia
| Evento | Destinatário | Conteúdo resumido |
|--------|--------------|-------------------|
| Item indisponível no pedido | Atendente | Aviso para propor substituição ao cliente |
| Estoque abaixo do mínimo | Gerente | Alerta com nome do insumo e quantidade restante |
| Fim do expediente | Gerente | Relatório de vendas do dia em PDF, por e-mail |

## 6. Entidades do banco (previsão inicial)
- **produtos**: id, nome, categoria, preco, disponivel
- **insumos**: id, nome, unidade_medida, quantidade_estoque, estoque_minimo
- **produto_insumo**: id, produto_id, insumo_id, quantidade_utilizada (ficha técnica de cada produto)
- **pedidos**: id, atendente_id, status, valor_total, criado_em
- **itens_pedido**: id, pedido_id, produto_id, quantidade, preco_unitario
- **usuarios**: id, nome, email, papel (atendente, cozinha, gerente)

## 7. Fora do escopo
- Integração com WhatsApp/API de mensagens (não faz parte da primeira versão)
- Pagamento online
- Aplicativo mobile nativo
- Delivery com rastreamento em tempo real
