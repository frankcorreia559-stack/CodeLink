import { useEffect, useState } from 'react'

function Feed() {
    const [posts, setPosts] = useState([])
    const [titulo, setTitulo] = useState('')
    const [conteudo, setConteudo] = useState('')
    const [mensagem, setMensagem] = useState('')
    const [carregando, setCarregando] = useState(true)
    const [publicando, setPublicando] = useState(false)

    async function carregarPosts() {
        try {
            const resposta = await fetch(
                'http://127.0.0.1:8000/posts'
            )

            const dados = await resposta.json()

            if (!resposta.ok) {
                setMensagem(
                    dados.detail || 'Não foi possível carregar os posts.'
                )
                return
            }

            setPosts(dados)

        } catch (erro) {
            console.error(erro)
            setMensagem('Erro ao conectar com a API.')
        } finally {
            setCarregando(false)
        }
    }

    useEffect(() => {
        carregarPosts()
    }, [])

    async function criarPost(event) {
        event.preventDefault()

        const token = localStorage.getItem('token')

        if (!token) {
            setMensagem('Você precisa estar logado.')
            return
        }

        if (!titulo.trim() || !conteudo.trim()) {
            setMensagem('Preencha o título e o conteúdo.')
            return
        }

        setPublicando(true)
        setMensagem('')

        try {
            const resposta = await fetch(
                'http://127.0.0.1:8000/posts',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        titulo: titulo,
                        conteudo: conteudo,
                    }),
                }
            )

            const dados = await resposta.json()

            if (!resposta.ok) {
                setMensagem(
                    dados.detail ||
                    'Não foi possível criar o post.'
                )
                return
            }

            setPosts((postsAtuais) => [
                dados,
                ...postsAtuais,
            ])

            setTitulo('')
            setConteudo('')
            setMensagem('Publicação criada com sucesso!')

        } catch (erro) {
            console.error(erro)
            setMensagem('Erro ao conectar com a API.')
        } finally {
            setPublicando(false)
        }
    }

    return (
        <div className="feed">

            <div className="create-post">

                <h2>📝 Criar publicação</h2>

                <form onSubmit={criarPost}>

                    <input
                        type="text"
                        placeholder="Título da publicação"
                        value={titulo}
                        onChange={(event) =>
                            setTitulo(event.target.value)
                        }
                    />

                    <textarea
                        placeholder="O que você está pensando?"
                        value={conteudo}
                        onChange={(event) =>
                            setConteudo(event.target.value)
                        }
                    />

                    <button
                        type="submit"
                        disabled={publicando}
                    >
                        {publicando
                            ? 'Publicando...'
                            : 'Publicar'}
                    </button>

                </form>

                {mensagem && (
                    <p style={{ marginTop: '12px' }}>
                        {mensagem}
                    </p>
                )}

            </div>

            <div className="posts">

                <h2>Feed do CodeLink</h2>

                {carregando ? (
                    <div className="post">
                        <p>Carregando publicações...</p>
                    </div>
                ) : posts.length === 0 ? (
                    <div className="post">
                        <p>
                            Nenhuma publicação ainda.
                            Seja o primeiro a publicar!
                        </p>
                    </div>
                ) : (
                    posts.map((post) => (
                        <article
                            className="post"
                            key={post.id}
                        >
                            <h3>{post.titulo}</h3>

                            <p>{post.conteudo}</p>

                            {post.autor && (
                                <small>
                                    Publicado por {post.autor.nome}
                                </small>
                            )}
                        </article>
                    ))
                )}

            </div>

        </div>
    )
}

export default Feed