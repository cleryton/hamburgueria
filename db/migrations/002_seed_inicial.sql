-- Migration 002: dados iniciais de exemplo (opcional, útil para testar a API)

INSERT INTO insumos (nome, unidade_medida, quantidade_estoque, estoque_minimo) VALUES
('Pao de burguer', 'un', 100, 20),
('Carne bovina 150g', 'un', 80, 15),
('Queijo cheddar', 'un', 90, 20),
('Alface', 'kg', 5, 1),
('Tomate', 'kg', 4, 1)
ON CONFLICT DO NOTHING;

INSERT INTO produtos (nome, categoria, preco, disponivel) VALUES
('X-Burguer', 'Lanches', 22.90, TRUE),
('X-Salada', 'Lanches', 25.90, TRUE),
('X-Bacon', 'Lanches', 28.90, TRUE)
ON CONFLICT DO NOTHING;
