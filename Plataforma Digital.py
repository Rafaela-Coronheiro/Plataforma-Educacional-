import json
import os
from statistics import mean, median, mode
from datetime import datetime
import matplotlib.pyplot as plt


def gerenciar_plataforma():
    inicializar_arquivos()
    while True:
        exibir_menu_principal()
        opcao = obter_opcao()
        executar_acao(opcao)


def inicializar_arquivos():
    arquivos = ['estudantes.json', 'cursos.json', 'notas.json']
    for arquivo in arquivos:
        if not os.path.exists(arquivo):
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False)


def exibir_menu_principal():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Registrar novo aluno")
    print("2. Visualizar cursos")
    print("3. Registrar notas")
    print("4. Ver estatísticas")
    print("5. Sair do sistema")


def obter_opcao():
    while True:
        try:
            opcao = int(input("\nOpção selecionada: "))
            if 1 <= opcao <= 5:
                return opcao
            print("Por favor, digite um número entre 1 e 5.")
        except ValueError:
            print("Entrada inválida. Digite um número.")


def executar_acao(opcao):
    acoes = {
        1: registrar_aluno,
        2: navegar_cursos,
        3: registrar_notas,
        4: exibir_estatisticas,
        5: sair_sistema
    }
    acao = acoes.get(opcao, opcao_invalida)
    acao()


def registrar_aluno():
    print("\n--- NOVO ALUNO ---")
    alunos = carregar_dados('estudantes.json')

    novo_id = max([aluno['id'] for aluno in alunos], default=0) + 1

    aluno = {
        "id": novo_id,
        "nome": input("Nome do aluno: ").title(),
        "idade": validar_idade(),
        "nivel": input("Nível (Iniciante/Intermediário/Avançado): ").title()
    }

    salvar_dados('estudantes.json', aluno)
    print(
        f"\n✅ Aluno {aluno['nome']} registrado com sucesso (ID: {aluno['id']})")


def validar_idade():
    while True:
        try:
            idade = int(input("Idade: "))
            if 5 <= idade <= 120:
                return idade
            print("Idade deve ser entre 5 e 120 anos.")
        except ValueError:
            print("Digite um número válido.")


def registrar_notas():
    print("\n--- REGISTRAR NOTAS ---")
    alunos = carregar_dados('estudantes.json')
    cursos = carregar_dados('cursos.json')
    notas = carregar_dados('notas.json')

    if not alunos:
        print("⚠️ Nenhum aluno cadastrado. Registre alunos primeiro.")
        return

    if not cursos:
        print("⚠️ Nenhum curso cadastrado. Registre cursos primeiro.")
        return

    print("\nLISTA DE ALUNOS:")
    for aluno in alunos:
        print(f"ID: {aluno['id']} | Nome: {aluno['nome']}")

    while True:
        try:
            aluno_id = int(input("\nDigite o ID do aluno: "))
            if not any(a['id'] == aluno_id for a in alunos):
                print("ID inválido. Tente novamente.")
                continue
            break
        except ValueError:
            print("Digite um número válido.")

    print("\nCURSOS DISPONÍVEIS:")
    for curso in cursos:
        print(f"ID: {curso['id']} | Curso: {curso['nome']}")

    while True:
        try:
            curso_id = int(input("\nDigite o ID do curso: "))
            if not any(c['id'] == curso_id for c in cursos):
                print("ID inválido. Tente novamente.")
                continue

            nota_existente = next(
                (n for n in notas if n['aluno_id'] == aluno_id and n['curso_id'] == curso_id), None)
            if nota_existente:
                print(
                    f"⚠️ Este aluno já possui nota {nota_existente['nota']} neste curso.")
                print("Deseja sobrescrever? (S/N)")
                if input().upper() != 'S':
                    return
                notas = [n for n in notas if not (
                    n['aluno_id'] == aluno_id and n['curso_id'] == curso_id)]
                with open('notas.json', 'w', encoding='utf-8') as f:
                    json.dump(notas, f, indent=2, ensure_ascii=False)
            break
        except ValueError:
            print("Digite um número válido.")

    while True:
        try:
            nota = float(input("\nDigite a nota (0-10): "))
            if 0 <= nota <= 10:
                break
            print("A nota deve ser entre 0 e 10.")
        except ValueError:
            print("Digite um número válido.")

    nova_nota = {
        "aluno_id": aluno_id,
        "curso_id": curso_id,
        "nota": round(nota, 1),
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    salvar_dados('notas.json', nova_nota)
    print(
        f"\n✅ Nota {nova_nota['nota']} registrada com sucesso em {nova_nota['data']}")


def navegar_cursos():
    cursos = carregar_cursos()
    while True:
        exibir_cursos(cursos)
        opcao = input(
            "\nPressione Enter para voltar ou digite o número do curso: ")
        if opcao == '':
            break
        mostrar_curso(cursos, opcao)


def carregar_cursos():
    cursos = carregar_dados('cursos.json')
    if not cursos:
        cursos = [
            {"id": 1, "nome": "Programação Python",
                "aulas": ["Sintaxe", "Funções", "POO"]},
            {"id": 2, "nome": "Banco de Dados", "aulas": [
                "SQL", "Modelagem", "Consultas"]},
            {"id": 3, "nome": "Análise de Dados", "aulas": [
                "Pandas", "Visualização", "Estatística"]}
        ]
        with open('cursos.json', 'w', encoding='utf-8') as f:
            json.dump(cursos, f, indent=2, ensure_ascii=False)
    return cursos


def exibir_cursos(cursos):
    print("\n--- CURSOS DISPONÍVEIS ---")
    for curso in cursos:
        print(f"\n{curso['id']}. {curso['nome']}")
        for aula in curso['aulas']:
            print(f"   - {aula}")


def mostrar_curso(cursos, opcao):
    try:
        curso_id = int(opcao)
        curso = next((c for c in cursos if c['id'] == curso_id), None)

        if curso:
            print(f"\n📚 CURSO: {curso['nome']}")
            print("\nAULAS:")
            for aula in curso['aulas']:
                print(f"  → {aula}")

            notas = carregar_dados('notas.json')
            notas_curso = [n['nota']
                           for n in notas if n['curso_id'] == curso_id]

            if notas_curso:
                print("\n📊 ESTATÍSTICAS:")
                print(f"Alunos: {len(notas_curso)}")
                print(f"Média: {mean(notas_curso):.1f}")
                print(f"Mediana: {median(notas_curso):.1f}")

                try:
                    print(f"Moda: {mode(notas_curso):.1f}")
                except:
                    print("Moda: Nenhuma moda única")

                plt.hist(notas_curso, bins=5,
                         color='skyblue', edgecolor='black')
                plt.title(f"Distribuição de Notas - {curso['nome']}")
                plt.xlabel("Notas")
                plt.ylabel("Quantidade de Alunos")
                plt.show()
            else:
                print("\nℹ️ Nenhuma nota registrada para este curso.")
        else:
            print("\n❌ Curso não encontrado!")
    except ValueError:
        print("\n❌ Digite um ID válido.")

    input("\nPressione Enter para continuar...")


def exibir_estatisticas():
    alunos = carregar_dados('estudantes.json')
    cursos = carregar_dados('cursos.json')
    notas = carregar_dados('notas.json')

    print("\n=== ESTATÍSTICAS GERAIS ===")

    if alunos:
        idades = [a['idade'] for a in alunos]
        print(f"\n👥 TOTAL ALUNOS: {len(alunos)}")
        print(f"📊 Média de idade: {mean(idades):.1f} anos")
        print(f"📊 Mediana: {median(idades)} anos")

        try:
            print(f"📊 Moda: {mode(idades)} anos")
        except:
            print("📊 Moda: Várias idades frequentes")

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.hist(idades, bins=5, color='lightgreen', edgecolor='black')
        plt.title("Distribuição de Idades")
        plt.xlabel("Idade")
        plt.ylabel("Quantidade")
    else:
        print("\n⚠️ Nenhum aluno registrado.")

    if notas:
        todas_notas = [n['nota'] for n in notas]
        print(f"\n🎯 TOTAL DE NOTAS REGISTRADAS: {len(notas)}")
        print(f"📈 Média geral: {mean(todas_notas):.1f}")
        print(f"📈 Mediana: {median(todas_notas):.1f}")

        try:
            print(f"📈 Moda: {mode(todas_notas):.1f}")
        except:
            print("📈 Moda: Várias notas frequentes")

        if alunos:
            plt.subplot(1, 2, 2)
        plt.hist(todas_notas, bins=5, color='lightcoral', edgecolor='black')
        plt.title("Distribuição de Notas")
        plt.xlabel("Nota")
        plt.ylabel("Quantidade")
        plt.tight_layout()
        plt.show()

        print("\n📚 DESEMPENHO POR CURSO:")
        for curso in cursos:
            notas_curso = [n['nota']
                           for n in notas if n['curso_id'] == curso['id']]
            if notas_curso:
                print(f"\n📌 {curso['nome']}:")
                print(f"   👥 Alunos: {len(notas_curso)}")
                print(f"   📊 Média: {mean(notas_curso):.1f}")
                print(f"   📊 Mediana: {median(notas_curso):.1f}")

                try:
                    print(f"   📊 Moda: {mode(notas_curso):.1f}")
                except:
                    print("   📊 Moda: Várias notas frequentes")

                medias = []
                cursos_com_notas = []
                for c in cursos:
                    nc = [n['nota'] for n in notas if n['curso_id'] == c['id']]
                    if nc:
                        medias.append(mean(nc))
                        cursos_com_notas.append(c['nome'])

                plt.figure(figsize=(8, 4))
                plt.bar(cursos_com_notas, medias, color=[
                        'skyblue', 'salmon', 'lightgreen'])
                plt.title("Média de Notas por Curso")
                plt.ylabel("Média")
                plt.ylim(0, 10)
                plt.show()
            else:
                print(f"\n📌 {curso['nome']}: Nenhuma nota registrada")
    else:
        print("\n⚠️ Nenhuma nota registrada.")

    input("\nPressione Enter para voltar...")


def carregar_dados(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_dados(arquivo, novo_registro):
    dados = carregar_dados(arquivo)
    dados.append(novo_registro)
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def opcao_invalida():
    print("Opção inválida! Tente novamente.")


def sair_sistema():
    print("\nSistema encerrado. Até mais!")
    exit()


if __name__ == '__main__':
    gerenciar_plataforma()
