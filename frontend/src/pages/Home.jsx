import Feed from './Feed'
import { useEffect, useState } from 'react'

function Home() {
    const [usuario, setUsuario] = useState(null)
    const [carregando, setCarregando] = useState(true)
    const [erro, setErro] = useState('')

    useEffect(() => {
        async function carregarUsuario() {
            const token = localStorage.getItem('token')

            if (!token) {
                setErro('Usuário não autenticado.')
                setCarregando(false)
                return
            }

            try {
                const resposta = await fetch(
                    'http://127.0.0.1:8000/usuarios/me',
                    {
                        method: 'GET',
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                )

                const dados = await resposta.json()

                if (!resposta.ok) {
                    setErro(
                        dados.detail ||
                        'Não foi possível carregar o usuário.'
                    )
                    return
                }

                setUsuario(dados)

            } catch (erro) {
                console.error(erro)
                setErro('Erro ao conectar com a API.')
            } finally {
                setCarregando(false)
            }
        }

        carregarUsuario()
    }, [])

    function sair() {
        localStorage.removeItem('token')
        window.location.reload()
    }

    if (carregando) {
        return (
            <div className="loading-screen">
                <div className="loading-card">
                    <h2>Carregando CodeLink...</h2>
                    <p>Preparando sua rede social.</p>
                </div>
            </div>
        )
    }

    if (erro) {
        return (
            <div className="error-screen">
                <div className="error-card">
                    <h2>Ops!</h2>
                    <p>{erro}</p>

                    <button onClick={sair}>
                        Voltar para o login
                    </button>
                </div>
            </div>
        )
    }

    return (
        <div className="codelink-layout">

            {/* SIDEBAR */}

            <aside className="sidebar">

                <div className="sidebar-logo">
                    <span>Code</span>Link
                </div>

                <div className="sidebar-profile">
                    <div className="profile-avatar">
                        {usuario?.nome?.charAt(0).toUpperCase()}
                    </div>

                    <strong>{usuario?.nome}</strong>

                    <small>
                        {usuario?.curso}
                    </small>
                </div>

                <nav className="sidebar-menu">

                    <button className="menu-item active">
                        🏠
                        <span>Início</span>
                    </button>

                    <button
                        className="menu-item"
                        onClick={() => {
                            window.location.href = '/perfil'
                        }}
                    >
                        👤
                        <span>Meu perfil</span>
                    </button>

                    <button className="menu-item">
                        👥
                        <span>Pessoas</span>
                    </button>

                    <button className="menu-item">
                        🔔
                        <span>Notificações</span>
                    </button>

                </nav>

                <div className="sidebar-bottom">

                    <button className="menu-item">
                        ⚙️
                        <span>Configurações</span>
                    </button>

                    <button
                        className="menu-item logout"
                        onClick={sair}
                    >
                        🚪
                        <span>Sair</span>
                    </button>

                </div>

            </aside>

            {/* CONTEÚDO PRINCIPAL */}

            <main className="main-content">

                <header className="topbar">

                    <div>
                        <h1>Início</h1>
                        <p>
                            Veja o que está acontecendo no CodeLink.
                        </p>
                    </div>

                    <div className="topbar-user">

                        <div className="notification">
                            🔔
                        </div>

                        <div className="top-avatar">
                            {usuario?.nome?.charAt(0).toUpperCase()}
                        </div>

                    </div>

                </header>

                <div className="content-grid">

                    {/* FEED */}

                    <section className="feed-area">
                        <Feed />
                    </section>

                    {/* PERFIL */}

                    <aside className="profile-card">

                        <div className="large-avatar">
                            {usuario?.nome?.charAt(0).toUpperCase()}
                        </div>

                        <h2>{usuario?.nome}</h2>

                        <p className="profile-course">
                            {usuario?.curso}
                        </p>

                        <p className="profile-bio">
                            {usuario?.bio || 'Adicione uma bio ao seu perfil.'}
                        </p>

                        <div className="profile-stats">

                            <div>
                                <strong>0</strong>
                                <span>Posts</span>
                            </div>

                            <div>
                                <strong>0</strong>
                                <span>Seguidores</span>
                            </div>

                            <div>
                                <strong>0</strong>
                                <span>Seguindo</span>
                            </div>

                        </div>

                        <button className="profile-button">
                            Ver perfil
                        </button>

                    </aside>

                </div>

            </main>

        </div>
    )
}

export default Home