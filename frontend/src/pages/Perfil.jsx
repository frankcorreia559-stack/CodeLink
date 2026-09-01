
import { useEffect, useState } from 'react'

function Perfil() {
    const [usuario, setUsuario] = useState(null)

    const [nome, setNome] = useState('')
    const [curso, setCurso] = useState('')
    const [bio, setBio] = useState('')
    const [foto, setFoto] = useState('')

    const [carregando, setCarregando] = useState(true)
    const [salvando, setSalvando] = useState(false)
    const [mensagem, setMensagem] = useState('')

    useEffect(() => {
        async function carregarPerfil() {
            const token = localStorage.getItem('token')

            if (!token) {
                setMensagem('Usuário não autenticado.')
                setCarregando(false)
                return
            }

            try {
                const resposta = await fetch(
                    'http://127.0.0.1:8000/usuarios/me',
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                )

                const dados = await resposta.json()

                if (!resposta.ok) {
                    setMensagem(
                        dados.detail ||
                        'Não foi possível carregar o perfil.'
                    )
                    return
                }

                setUsuario(dados)
                setNome(dados.nome || '')
                setCurso(dados.curso || '')
                setBio(dados.bio || '')
                setFoto(dados.foto || '')

            } catch (erro) {
                console.error(erro)
                setMensagem('Erro ao conectar com a API.')
            } finally {
                setCarregando(false)
            }
        }

        carregarPerfil()
    }, [])

    async function salvarPerfil(event) {
        event.preventDefault()

        const token = localStorage.getItem('token')

        if (!token) {
            setMensagem('Usuário não autenticado.')
            return
        }

        setSalvando(true)
        setMensagem('')

        try {
            const resposta = await fetch(
                'http://127.0.0.1:8000/usuarios/me',
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        nome,
                        curso,
                        bio,
                        foto,
                    }),
                }
            )

            const dados = await resposta.json()

            if (!resposta.ok) {
                setMensagem(
                    dados.detail ||
                    'Não foi possível atualizar o perfil.'
                )
                return
            }

            setUsuario(dados)

            setNome(dados.nome || '')
            setCurso(dados.curso || '')
            setBio(dados.bio || '')
            setFoto(dados.foto || '')

            setMensagem('Perfil atualizado com sucesso!')

        } catch (erro) {
            console.error(erro)
            setMensagem('Erro ao conectar com a API.')
        } finally {
            setSalvando(false)
        }
    }

    if (carregando) {
        return (
            <div className="loading-screen">
                <div className="loading-card">
                    <h2>Carregando perfil...</h2>
                </div>
            </div>
        )
    }

    return (
        <div className="profile-page">

            <div className="profile-header">

                <div className="large-avatar">
                    {usuario?.nome?.charAt(0).toUpperCase()}
                </div>

                <h1>{usuario?.nome}</h1>

                <p>{usuario?.curso}</p>

            </div>

            <div className="profile-edit-card">

                <h2>Editar perfil</h2>

                <form onSubmit={salvarPerfil}>

                    <div className="form-group">
                        <label>Nome</label>

                        <input
                            type="text"
                            value={nome}
                            onChange={(event) =>
                                setNome(event.target.value)
                            }
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Curso</label>

                        <input
                            type="text"
                            value={curso}
                            onChange={(event) =>
                                setCurso(event.target.value)
                            }
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Bio</label>

                        <textarea
                            value={bio}
                            onChange={(event) =>
                                setBio(event.target.value)
                            }
                            placeholder="Conte um pouco sobre você..."
                        />
                    </div>

                    <div className="form-group">
                        <label>URL da foto</label>

                        <input
                            type="url"
                            value={foto}
                            onChange={(event) =>
                                setFoto(event.target.value)
                            }
                            placeholder="https://..."
                        />
                    </div>

                    <button
                        type="submit"
                        className="profile-save-button"
                        disabled={salvando}
                    >
                        {salvando
                            ? 'Salvando...'
                            : 'Salvar alterações'}
                    </button>

                </form>

                {mensagem && (
                    <p className="profile-message">
                        {mensagem}
                    </p>
                )}

            </div>

        </div>
    )
}

export default Perfil

