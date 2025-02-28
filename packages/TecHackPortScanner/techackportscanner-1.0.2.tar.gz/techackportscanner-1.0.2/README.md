# Projeto TecHack - Roteiro 1

## Descrição
Este projeto é parte do curso TecHack da Insper. O objetivo deste roteiro é introduzir conceitos básicos de programação e desenvolvimento de software.

## Funcionalidades

- Suporte para IPv4
- Suporte para IPv6
- Suporte para Porta especifica ou Range
- Escaneamento de Rede usando CIDR
- Escaneamento de portas TCP
- Escaneamento de portas UDP
- Detecção de sistema operacional
- Detecção de serviços de rede atravez de Well-Know Ports
- Suporte para procura de serviço na rede
- Detecção do STATUS da porta
- Suporte a argumentos de linha de comando

## Estrutura do Projeto

- `scanner/`
  - `__init__.py`: Inicializa o pacote e importa as funções principais.
  - `detector.py`: Contém funções para detectar serviços de rede e manipular argumentos de requisição.
  - `scan_manager.py`: Fornece funções para escaneamento TCP e UDP, bem como detecção de sistema operacional.
  - `consts.py`: Define constantes usadas em todo o pacote.
  - `args_parser.py`: Analisa e valida os argumentos fornecidos pelo usuário.

## Requisitos
- Python 3.9+
- scapy

## Instalação
1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/seu-repositorio.git
    ```
2. Navegue até o diretório do projeto:
    ```sh
    cd seu-repositorio
    ```
3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

    ## Uso
    Para executar o projeto, utilize o seguinte comando:
    ```sh
    python -m scanner <args>
    ```
### Exemplos de Uso

python -m scanner 192.168.0.1
python -m scanner 192.168.1.1 -p 22,80,443
python -m scanner 192.168.1.1 -p 53,123 --udp
python -m scanner 192.168.1.0/24 --service ssh

## Contribuição
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Faça o push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato
Para mais informações, entre em contato com [admin@peng1104.net](mailto:admin@peng1104.net).