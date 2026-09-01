
import { useState } from 'react'

function Login() {
    const [email, setEmail] = useState('')
    const [senha, setSenha] = useState('')
    const [mensagem, setMensagem] = useState('')
    const [carregando, setCarregando] = useState(false)

    async function handleLogin(event) {
        event.preventDefault()

        setMensagem('')
        setCarregando(true)

        try {
            const dadosLogin = new URLSearchParams()

            dadosLogin.append('username', email)
            dadosLogin.append('password', senha)

            const resposta = await fetch('http://127.0.0.1:8000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: dadosLogin,
            })

            const dados = await resposta.json()

            if (!resposta.ok) {
                setMensagem(
                    dados.detail || 'E-mail ou senha incorretos.'
                )
                return
            }

            localStorage.setItem('token', dados.access_token)

            setMensagem('Login realizado com sucesso!')

            setMensagem('Login realizado com sucesso!')

            setTimeout(() => {
                window.location.href = '/home'
            }, 500)

        } catch (erro) {
            console.error('Erro ao fazer login:', erro)

            setMensagem(
                'Não foi possível conectar com a API.'
            )
        } finally {
            setCarregando(false)
        }
    }

    return (
        <div className="login-page">

            <div className="login-card">

                <h1>CodeLink</h1>

                <p className="login-subtitle">
                    Entre na sua conta
                </p>

                <form onSubmit={handleLogin}>

                    <div className="form-group">
                        <label>Email</label>

                        <input
                            type="email"
                            placeholder="Digite seu email"
                            value={email}
                            onChange={(event) => setEmail(event.target.value)}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Senha</label>

                        <input
                            type="password"
                            placeholder="Digite sua senha"
                            value={senha}
                            onChange={(event) => setSenha(event.target.value)}
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="login-button"
                        disabled={carregando}
                    >
                        {carregando ? 'Entrando...' : 'Entrar'}
                    </button>

                </form>

                {mensagem && (
                    <p className="login-message">
                        {mensagem}
                    </p>
                )}

                <p className="register-text">
                    Ainda não possui uma conta?

                    <button
                        type="button"
                        className="register-link"
                    >
                        Criar conta
                    </button>
                </p>

            </div>

        </div>
    )
}

export default Login

