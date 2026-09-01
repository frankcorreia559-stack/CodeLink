
import { useState } from "react";

function Login() {
    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");
    const [mensagem, setMensagem] = useState("");
    const [carregando, setCarregando] = useState(false);

    async function fazerLogin(e) {
        e.preventDefault();

        setMensagem("");
        setCarregando(true);

        try {
            const dados = new URLSearchParams();

            dados.append("username", email);
            dados.append("password", senha);

            const resposta = await fetch("http://127.0.0.1:8000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: dados,
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                throw new Error(
                    resultado.detail || "E-mail ou senha incorretos."
                );
            }

            // Salva o token JWT
            localStorage.setItem(
                "token",
                resultado.access_token
            );

            setMensagem("Login realizado com sucesso!");

            console.log("Token recebido:", resultado.access_token);

        } catch (erro) {
            console.error("Erro no login:", erro);
            setMensagem(erro.message);
        } finally {
            setCarregando(false);
        }
    }

    return (
        <div>
            <h1>CodeLink</h1>

            <h2>Login</h2>

            <form onSubmit={fazerLogin}>

                <div>
                    <label>E-mail</label>

                    <input
                        type="email"
                        placeholder="Digite seu e-mail"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>

                <div>
                    <label>Senha</label>

                    <input
                        type="password"
                        placeholder="Digite sua senha"
                        value={senha}
                        onChange={(e) => setSenha(e.target.value)}
                        required
                    />
                </div>

                <button type="submit" disabled={carregando}>
                    {carregando ? "Entrando..." : "Entrar"}
                </button>

            </form>

            {mensagem && (
                <p>{mensagem}</p>
            )}
        </div>
    );
}

export default Login;

