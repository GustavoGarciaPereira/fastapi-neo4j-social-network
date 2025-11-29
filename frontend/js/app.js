// Configuração da API
const API_BASE_URL = 'http://localhost:8000';

// Elementos DOM
let pessoasCache = [];

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
  carregarPessoas();
  carregarEstatisticas();
  document.getElementById('person-form').addEventListener('submit', adicionarPessoa);
  initThemeToggle();
});

function initThemeToggle() {
  const toggle = document.getElementById('theme-toggle');
  const root = document.documentElement;
  const stored = localStorage.getItem('theme') || 'light';
  root.setAttribute('data-theme', stored);
  toggle.innerHTML = stored === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';

  toggle.addEventListener('click', () => {
    const current = root.getAttribute('data-theme');
    const next = current === 'light' ? 'dark' : 'light';
    root.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    toggle.innerHTML = next === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
  });
}
// Funções de Loading
let loadingCount = 0;
let isLocked = false;
const MIN_SPINNER_TIME = 1000; // 4 segundos
let spinnerStart = 0;

function showLoading(message = 'Sincronizando dados...') {
  if (message) {
    document.querySelector('#loading p').textContent = message;
  }

  const loadingEl = document.getElementById('loading');

  // registra início somente quando o overlay sai do estado hidden
  if (loadingCount === 0) {
    spinnerStart = Date.now();
    loadingEl.classList.remove('hidden');
  }

  loadingCount++;
}

function hideLoading(force = false) {
  if (isLocked && !force) return;

  loadingCount = Math.max(loadingCount - 1, 0);

  if (loadingCount === 0) {
    const elapsed = Date.now() - spinnerStart;
    const delay = Math.max(0, MIN_SPINNER_TIME - elapsed);

    setTimeout(() => {
      if (loadingCount === 0) {
        document.getElementById('loading').classList.add('hidden');
      }
    }, delay);
  }
}
function hideLoading(force = false) {
  if (isLocked && !force) return;

  loadingCount = Math.max(loadingCount - 1, 0);
  if (loadingCount === 0) {
    document.getElementById('loading').classList.add('hidden');
  }
}

function lockLoading(message = 'Sincronizando dados...') {
  isLocked = true;
  showLoading(message);
}

function unlockLoading() {
  isLocked = false;
  hideLoading(true); // força esconder depois que o lock terminar
}

// API Functions
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro na chamada da API:', error);
        // Não alerta aqui, deixa cada função tratar o erro
        throw error; // Continua propagando o erro
    }
}

// Carregar Pessoas
async function carregarPessoas() {
  showLoading();
  try {
    const pessoas = await apiCall('/pessoas/');
    renderizarPessoas(pessoas);
  } catch (error) {
    console.error('Erro ao carregar pessoas:', error);
  } finally {
    hideLoading();
  }
}
// Carregar Estatísticas
async function carregarEstatisticas() {
    try {
        const stats = await apiCall('/estatisticas/');
        renderizarEstatisticas(stats);
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

// Adicionar Pessoa
// Adicionar Pessoa
async function adicionarPessoa(event) {
    event.preventDefault();
    
    const nome = document.getElementById('nome').value;
    const idade = parseInt(document.getElementById('idade').value);
    const cidade = document.getElementById('cidade').value;
    const interessesInput = document.getElementById('interesses').value;
    const interesses = interessesInput ? 
        interessesInput.split(',').map(i => i.trim()) : [];
    
    const pessoaData = {
        nome: nome,
        idade: idade,
        cidade: cidade || '',
        interesses: interesses
    };
    
    showLoading();
    try {
        await apiCall('/pessoas/', {
            method: 'POST',
            body: JSON.stringify(pessoaData)
        });
        
        event.target.reset();
        await carregarPessoas();
        await carregarEstatisticas();
        
        alert('Pessoa adicionada com sucesso!');
    } catch (error) {
        console.error('Erro ao adicionar pessoa:', error);
        alert('Erro ao adicionar pessoa.');
    } finally {
        hideLoading();
    }
}
// Buscar por Interesse
async function buscarPorInteresse() {
    const interesse = document.getElementById('interesse-busca').value.trim();
    
    if (!interesse) {
        alert('Por favor, digite um interesse para buscar.');
        return;
    }
    
    showLoading();
    try {
        const resultados = await apiCall(`/pessoas/interesse/${encodeURIComponent(interesse)}`);
        renderizarResultadosBusca(resultados, interesse);
    } catch (error) {
        console.error('Erro na busca:', error);
    } finally {
        hideLoading();
    }
}

// Ver Detalhes da Pessoa
async function verDetalhes(pessoaId) {
    showLoading();
    try {
        const [pessoa, amigos, similares, rede] = await Promise.all([
            apiCall(`/pessoas/${pessoaId}`),
            apiCall(`/pessoas/${pessoaId}/amigos`),
            apiCall(`/pessoas/${pessoaId}/similares`),
            apiCall(`/pessoas/${pessoaId}/rede/2`)
        ]);
        
        renderizarDetalhesPessoa(pessoa, amigos, similares, rede);
    } catch (error) {
        console.error('Erro ao carregar detalhes:', error);
    } finally {
        hideLoading();
    }
}

// Ver Rede Social
async function verRedeSocial(pessoaId, nomePessoa) {
    showLoading();
    try {
        const rede = await apiCall(`/pessoas/${pessoaId}/rede/3`);
        renderizarRedeSocial(rede, nomePessoa);
    } catch (error) {
        console.error('Erro ao carregar rede:', error);
    } finally {
        hideLoading();
    }
}
// Renderização
function renderizarPessoas(pessoas) {
    const container = document.getElementById('pessoas-list');
    
    if (pessoas.length === 0) {
        container.innerHTML = '<p>Nenhuma pessoa cadastrada.</p>';
        return;
    }
    
    container.innerHTML = pessoas.map(pessoa => `
        <div class="pessoa-card fade-in" onclick="verDetalhes(${pessoa.id})">
            <h4>${pessoa.nome}</h4>
            <div class="pessoa-info">
                <i class="fas fa-birthday-cake"></i> ${pessoa.idade} anos
            </div>
            <div class="pessoa-info">
                <i class="fas fa-city"></i> ${pessoa.cidade || 'Não informada'}
            </div>
            ${pessoa.interesses && pessoa.interesses.length > 0 ? `
                <div class="interesses">
                    ${pessoa.interesses.map(interesse => 
                        `<span class="interesse-tag">${interesse}</span>`
                    ).join('')}
                </div>
            ` : ''}
        </div>
    `).join('');
}

function renderizarEstatisticas(stats) {
    const container = document.getElementById('stats-content');
    
    container.innerHTML = `
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: var(--primary);">${stats.total_pessoas}</div>
                <div style="font-size: 0.9rem; color: var(--text-light);">Pessoas</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: var(--success);">${stats.total_relacionamentos}</div>
                <div style="font-size: 0.9rem; color: var(--text-light);">Relacionamentos</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: var(--warning);">${stats.densidade_rede}</div>
                <div style="font-size: 0.9rem; color: var(--text-light);">Densidade</div>
            </div>
        </div>
        
        ${stats.top_interesses && stats.top_interesses.length > 0 ? `
            <div style="margin-top: 15px;">
                <strong>Interesses Populares:</strong><br>
                ${stats.top_interesses.map(item => 
                    `${item.interesse} (${item.quantidade})`
                ).join(', ')}
            </div>
        ` : ''}
    `;
}

function renderizarResultadosBusca(resultados, interesse) {
    const container = document.getElementById('resultados-busca');
    
    if (resultados.length === 0) {
        container.innerHTML = `<p>Nenhuma pessoa encontrada com o interesse "${interesse}".</p>`;
        return;
    }
    
    container.innerHTML = `
        <p><strong>${resultados.length} pessoas encontradas com "${interesse}":</strong></p>
        <div style="margin-top: 10px;">
            ${resultados.map(pessoa => `
                <div class="pessoa-card" onclick="verDetalhes(${pessoa.id})">
                    <h4>${pessoa.nome}</h4>
                    <div>${pessoa.idade} anos • ${pessoa.cidade || 'Não informada'}</div>
                </div>
            `).join('')}
        </div>
    `;
}

function renderizarDetalhesPessoa(pessoa, amigos, similares, rede) {
    const container = document.getElementById('detalhes-conteudo');
    const titulo = document.getElementById('detalhes-titulo');
    
    titulo.textContent = `Detalhes: ${pessoa.nome}`;
    
    container.innerHTML = `
        <div class="detalhes-section">
            <h4><i class="fas fa-info-circle"></i> Informações</h4>
            <p><strong>Idade:</strong> ${pessoa.idade} anos</p>
            <p><strong>Cidade:</strong> ${pessoa.cidade || 'Não informada'}</p>
            <p><strong>Interesses:</strong> ${pessoa.interesses ? pessoa.interesses.join(', ') : 'Nenhum'}</p>
        </div>
        
        <div class="detalhes-section">
            <h4><i class="fas fa-user-friends"></i> Amigos (${amigos.length})</h4>
            ${amigos.length > 0 ? `
                <div class="amigos-list">
                    ${amigos.map(amigo => `
                        <div class="conexao-item">
                            <div class="conexao-info">
                                <h4>${amigo.nome}</h4>
                                <div>${amigo.idade} anos • ${amigo.cidade || 'Não informada'}</div>
                            </div>
                            <button onclick="verDetalhes(${amigo.id})" class="btn-refresh">
                                <i class="fas fa-eye"></i> Ver
                            </button>
                        </div>
                    `).join('')}
                </div>
            ` : '<p>Nenhum amigo encontrado.</p>'}
        </div>
        
        <div class="detalhes-section">
            <h4><i class="fas fa-user-plus"></i> Pessoas Similares</h4>
            ${similares.length > 0 ? `
                <div class="similares-list">
                    ${similares.map(similar => `
                        <div class="conexao-item">
                            <div class="conexao-info">
                                <h4>${similar.nome}</h4>
                                <div>${similar.idade} anos • ${similar.cidade || 'Não informada'}</div>
                                <div><small>Interesses em comum: ${similar.interesses_comuns.join(', ')}</small></div>
                            </div>
                            <button onclick="verDetalhes(${similar.id})" class="btn-refresh">
                                <i class="fas fa-eye"></i> Ver
                            </button>
                        </div>
                    `).join('')}
                </div>
            ` : '<p>Nenhuma pessoa similar encontrada.</p>'}
        </div>
        
        <div class="detalhes-actions">
            <button onclick="verRedeSocial(${pessoa.id}, '${pessoa.nome}')" class="btn-refresh">
                <i class="fas fa-network-wired"></i> Ver Rede Social
            </button>
        </div>
    `;
    
    document.getElementById('pessoa-detalhes').classList.remove('hidden');
}

function renderizarRedeSocial(rede, nomePessoa) {
    const container = document.getElementById('rede-conteudo');
    const titulo = document.getElementById('rede-titulo');
    
    titulo.textContent = `Rede Social: ${nomePessoa}`;
    
    if (rede.length === 0) {
        container.innerHTML = '<p>Nenhuma conexão encontrada na rede.</p>';
    } else {
        container.innerHTML = `
            <p><strong>${rede.length} conexões encontradas na rede:</strong></p>
            <div style="margin-top: 15px;">
                ${rede.map(pessoa => `
                    <div class="conexao-item">
                        <div class="conexao-info">
                            <h4>${pessoa.nome}</h4>
                            <div>${pessoa.idade} anos • ${pessoa.cidade || 'Não informada'}</div>
                            ${pessoa.interesses && pessoa.interesses.length > 0 ? `
                                <div><small>Interesses: ${pessoa.interesses.join(', ')}</small></div>
                            ` : ''}
                        </div>
                        <div class="conexao-actions">
                            <button onclick="verDetalhes(${pessoa.id})" class="btn-refresh">
                                <i class="fas fa-eye"></i> Ver
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    document.getElementById('rede-social').classList.remove('hidden');
}

// Funções de UI
function fecharDetalhes() {
    document.getElementById('pessoa-detalhes').classList.add('hidden');
}

function fecharRede() {
    document.getElementById('rede-social').classList.add('hidden');
}

// Função para criar relacionamento (extra)
async function criarRelacionamento(pessoaId1, pessoaId2) {
    if (!confirm('Deseja criar um relacionamento entre estas pessoas?')) {
        return;
    }
    
    showLoading();
    try {
        await apiCall(`/pessoas/${pessoaId1}/conhece/${pessoaId2}`, {
            method: 'POST'
        });
        
        alert('Relacionamento criado com sucesso!');
        await carregarPessoas();
        await carregarEstatisticas();
    } catch (error) {
        console.error('Erro ao criar relacionamento:', error);
        alert('Erro ao criar relacionamento.');
    } finally {
        hideLoading();
    }
}