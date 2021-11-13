# Kanvas

## Descrição
O __Kanvas__ é um sistema desenvolvidos para instituições de ensino, com o objetivo de automatizar as seguintes tarefas: registrar alunos, instrutores e facilitadores de ensino; registrar cursos e atividades; guardar envios de atividades dos alunos e envios de notas, feitas por instrutores/facilitadores, destas atividades.

## Instalação
Para instalar o sistema, é necessário seguir alguns passos, como baixar o projeto e fazer instalação das dependências. Para isso, é necessário abrir uma aba do terminal e digitar o seguinte:

    # Baixar o projeto:
        git clone https://gitlab.com/charles_pinheiro/kanvas

    # Entrar na pasta:
        cd kanvas

    # Criar ambiente virtual:
        python3 -m venv venv

    # Entrar no ambiente virtual:
        source venv/bin/activate

    # Instalar dependências:
        pip install -r requirements.txt

Depois de ter instalado as dependências, é necessário rodar as migrations para que o banco de dados e as tabelas sejam criadas:

    # python manage.py migrate

Por fim, para rodar o projeto:

    # python manage.py runserver

## Utilização

### Rotas

#### POST /api/accounts/
Criação de usuários.

    # RESPONSE STATUS -> HTTP 201 (CREATED)

__Body:__

    {
        "username": "student3",
        "password": "1234",
        "is_superuser": false,
        "is_staff": false
    }
* estudante => is_superuser e is_staff: False
* facilitador => is_staff: True
* instrutor => is_superuser: True

__Response:__

    {
        "id": 1,
        "username": "student",
        "is_superuser": false,
        "is_staff": false
    }

#### POST /api/login/
Autenticação do usuário.

    # RESPONSE STATUS -> HTTP 200 (OK)

__Body:__

    {
        "username": "student",
        "password": "1234"
    }

__Response:__

    {
        "token": "a4900d46d2eb91a419a61cd92f4d9075205adf22"
    }

#### POST /api/courses/
Criação de curso.

    # RESPONSE STATUS -> HTTP 201 (CREATED)

* Autenticação de Instrutor

__Body:__

    {
        "name": "Curso"
    }

__Response:__

    {
        "id": 1,
        "name": "Curso",
        "users": []
    }

#### GET /api/courses/
Lista os cursos e os alunos matriculados.

    # RESPONSE STATUS -> HTTP 200 (OK)

__Response:__

    {
        "id": 1,
        "name": "Curso",
        "users": [
            {
                "id": 1,
                "username": "student"
            }
        ]
    }

#### GET /api/courses/int:course_id/
Retorna o curso com o id informado.

    # RESPONSE STATUS -> HTTP 200 (OK)

__Response:__

    {
        "id": 1,
        "name": "Q1",
        "users": [
            {
                "id": 1,
                "username": "student"
            }
        ]
    }

#### PUT /api/courses/int:course_id/
Altera nome do curso.

    # RESPONSE STATUS -> HTTP 200 (OK)

* Autenticação de Instrutor

__Body:__

    {
        "name": "Curso Novo"
    }

__Response:__

    {
        "id": 1,
        "name": "Q4",
        "users": [
            {
                "id": 1,
                "username": "student"
            }
        ]
    }

#### DELETE /api/courses/int:course_id/
Deleta o curso.

    # RESPONSE STATUS -> HTTP 204 (NO CONTENT)

* Autenticação de Instrutor

#### PUT /api/courses/int:course_id/registrations/
Vincula os alunos ao curso.

    # RESPONSE STATUS -> HTTP 200 (OK)

* Autenticação de Instrutor

__Body:__

    {
        "user_ids": [1]
    }

__Response:__

    {
        "id": 1,
        "name": "Curso",
        "users": [
            {
                "id": 1,
                "username": "student"
            }
        ]
    }

#### POST /api/activities/
Cria uma nova atividade.

    # RESPONSE STATUS -> HTTP 201 (CREATED)

* Autenticação de Instrutor ou Facilitador

__Body:__

    {
        "title": "Atividade",
        "points": 10
    }

__Response:__

    {
        "id": 1,
        "title": "Atividade",
        "points": 10.0,
        "submissions": []
    }

#### GET /api/activities/
Lista todas as atividades com suas respectivas submissões.

    # RESPONSE STATUS -> HTTP 200 (OK)

* Autenticação de Instrutor ou Facilitador

__Response:__

    {
        [
            {
                "id": 1,
                "title": "Kenzie Pet",
                "points": 10,
                "submissions": [
                    {
                        "id": 1,
                        "grade": 10,
                        "repo": "http://gitlab.com/kenzie_pet",
                        "user_id": 3,
                        "activity_id": 1
                    }
                ]
            },
            {
                "id": 2,
                "title": "Kanvas",
                "points": 10,
                "submissions": [
                    {
                        "id": 2,
                        "grade": 8,
                        "repo": "http://gitlab.com/kanvas",
                        "user_id": 4,
                        "activity_id": 2
                    }
                ]
            },
            ...
        ]
    }

#### PUT /api/activities/int:activity_id/
Editar uma atividade.

    # RESPONSE STATUS -> HTTP 200 (OK)

* Autenticação de Instrutor ou Facilitador

__Body:__

    {
	    "title": "Atividade nova",
	    "points": 20
    }

__Response:__

    {
      "id": 1,
      "title": "Atividade nova",
      "points": 20.0,
      "submissions": []
    }

#### POST /api/activities/int:activity_id/submissions/
Faz a submissão de uma atividade.

    # RESPONSE STATUS -> HTTP 201 (CREATED)

* Autenticação de Aluno

__Body:__

    {
	    "repo": "http://gitlab.com/atividade_5"
    }

__Response:__

    {
        "id": 7,
        "grade": null,
        "repo": "http://gitlab.com/atividade_5",
        "user_id": 3,
        "activity_id": 1
    }

#### PUT /api/submissions/int:submission_id/
Altera a nota de uma submissão.

    # RESPONSE STATUS -> HTTP 200 (OK)

* Autenticação de Instrutor ou Facilitador

__Body:__

    {
        "grade": 10
    }

__Response:__

    {
        "id": 1,
        "grade": 10.0,
        "repo": "http://gitlab.com/atividade_5",
        "user_id": 1,
        "activity_id": 1
    }

#### GET /api/submissions/
Lista as submissões.

    # RESPONSE STATUS -> HTTP 200 (OK)

* Com autenticação de Aluno: Retorna apenas as submissões do aluno autenticado.

__Body:__

    [
        {
          "id": 1,
          "grade": 10.0,
          "repo": "http://gitlab.com/atividade_5",
          "user_id": 1,
          "activity_id": 1
        },
        {
          "id": 2,
          "grade": null,
          "repo": "http://gitlab.com/atividade_6",
          "user_id": 1,
          "activity_id": 1
        }
    ]

* Com autenticação de Instrutor ou Facilitador: Retorna as submissões de todos os alunos.

__Body:__

    [
    {
      "id": 1,
      "grade": 10.0,
      "repo": "http://gitlab.com/atividade_5",
      "user_id": 1,
      "activity_id": 1
    },
    {
      "id": 2,
      "grade": null,
      "repo": "http://gitlab.com/atividade_6",
      "user_id": 1,
      "activity_id": 1
    },
    {
      "id": 3,
      "grade": null,
      "repo": "http://gitlab.com/atividade_6",
      "user_id": 3,
      "activity_id": 1
    }
    ]