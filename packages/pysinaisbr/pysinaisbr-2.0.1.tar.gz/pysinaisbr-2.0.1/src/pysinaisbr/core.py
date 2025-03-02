"""
PySinaisBR - Biblioteca brasileira para processamento de sinais e sistemas
Autor: Matheus Sousa
Versão: 2.0.1 (Otimizada)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fht, fftshift
from scipy import signal
from scipy.integrate import quad
import pywt
from reedsolo import RSCodec
from numba import njit

class Transformadas:
    @staticmethod
    @njit(cache=True)
    def _precalc_fourier(N, T):
        freq = np.fft.fftfreq(N, T)[:N//2]
        return freq, 2.0/N
    
    @classmethod
    def fourier(cls, sinal, dominio_tempo):
        N = len(sinal)
        T = dominio_tempo[1] - dominio_tempo[0]
        freq, fator = cls._precalc_fourier(N, T)
        espectro = fft(sinal)
        return freq, fator * np.abs(espectro[:N//2])

    @staticmethod
    def inversa_fourier(espectro):
        return ifft(espectro).real

    @staticmethod
    def wavelet(sinal, wavelet='db1', nivel=4):
        return pywt.wavedec(sinal, wavelet, level=nivel, mode='periodization')

    @staticmethod
    def hartley(sinal):
        return fht(sinal)

    @staticmethod
    def laplace(funcao_tempo, sigma_max=10, pontos=500):
        sigma = np.linspace(0, sigma_max, pontos)
        t = np.logspace(-6, 6, 100000)
        dt = np.diff(t)
        t = t[:-1]
        
        transformada = np.empty(pontos, dtype=np.complex128)
        for i, s in enumerate(sigma):
            integrando = funcao_tempo(t) * np.exp(-s * t)
            transformada[i] = np.sum(integrando * dt)
        return sigma, transformada

    @staticmethod
    @njit
    def _z_transform(sinal, amostras):
        n = len(sinal)
        z = np.exp(1j * amostras)
        k = np.arange(n)
        return z, np.sum(sinal * z ** -k[:, None], axis=0)

    @classmethod
    def z(cls, sinal, amostras=None):
        n = len(sinal)
        if amostras is None:
            amostras = np.linspace(0, 2*np.pi, n)
        z, transformada = cls._z_transform(sinal, amostras)
        return z, transformada

    @staticmethod
    def inversa_z(transformada_z):
        return np.fft.ifft(transformada_z).real

class ModulacaoDigital:
    _qpsk_map = np.array([1+1j, 1-1j, -1+1j, -1-1j]) / np.sqrt(2)
    _qam16_map = np.array([
        -3-3j, -3-1j, -3+3j, -3+1j,
        -1-3j, -1-1j, -1+3j, -1+1j,
        3-3j,  3-1j,  3+3j,  3+1j,
        1-3j,  1-1j,  1+3j,  1+1j
    ]) / np.sqrt(10)

    @classmethod
    def qpsk(cls, bits):
        bits = np.asarray(bits, dtype=np.uint8)
        simbolos = bits.reshape(-1, 2)
        indices = 2*simbolos[:,0] + simbolos[:,1]
        return cls._qpsk_map[indices], simbolos

    @classmethod
    def qam16(cls, bits):
        bits = np.asarray(bits, dtype=np.uint8)
        simbolos = bits.reshape(-1, 4)
        indices = 8*simbolos[:,0] + 4*simbolos[:,1] + 2*simbolos[:,2] + simbolos[:,3]
        return cls._qam16_map[indices], simbolos

class CompressaoSinais:
    @staticmethod
    @njit
    def dpcm(sinal, bits_quantizacao=8):
        diferenca = np.empty_like(sinal)
        diferenca[0] = sinal[0]
        for i in range(1, len(sinal)):
            diferenca[i] = sinal[i] - sinal[i-1]
        
        q_max = 2**(bits_quantizacao-1)
        q_step = (np.max(diferenca) - np.min(diferenca)) / (2*q_max)
        return np.round(diferenca / q_step) * q_step

    @staticmethod
    @njit
    def adpcm(sinal, ordem=2):
        n = len(sinal)
        pred = np.zeros(n)
        coefs = np.zeros(ordem+1)
        
        for i in range(ordem, n):
            X = np.vander(sinal[i-ordem:i], ordem+1)
            coefs = np.linalg.lstsq(X, sinal[i-ordem:i])[0]
            pred[i] = np.dot(coefs, sinal[i-ordem:i][::-1])
        
        erro = sinal - pred
        return erro, coefs

class SistemasLineares:
    @staticmethod
    def resposta_impulso(num, den, tempo):
        sistema = signal.TransferFunction(num, den)
        t, resposta = signal.impulse(sistema, T=tempo)
        return t, resposta

    @staticmethod
    def analise_estabilidade(num, den):
        polos = np.roots(den)
        zeros = np.roots(num)
        return {
            'polos': polos,
            'zeros': zeros,
            'estavel': all(np.abs(polos) < 1),
            'margem_ganho': signal.margin((num, den))[0]
        }

class CodificacaoCanal:
    def __init__(self, t_correcao=2):
        self.rsc = RSCodec(t_correcao)
        self.G = np.array([[1,1,0,1], [1,0,1,1], [0,1,1,1]])
    
    @njit
    def codificar_hamming(self, dados):
        dados = np.asarray(dados).reshape(-1, 4)
        bits_paridade = np.dot(dados, self.G.T) % 2
        return np.hstack((dados, bits_paridade)).flatten()

    def codificar_reed_solomon(self, dados):
        return self.rsc.encode(dados)

    def decodificar_reed_solomon(self, dados):
        return self.rsc.decode(dados)

class ProcessamentoSinal:
    @staticmethod
    @njit
    def amostrar(sinal, taxa_original, taxa_nova):
        n = int(len(sinal) * taxa_nova / taxa_original)
        return np.interp(
            np.linspace(0, len(sinal)-1, n),
            np.arange(len(sinal)),
            sinal
        )

    @staticmethod
    def filtrar(sinal, freq_corte, taxa_amostragem, tipo='passa-baixas'):
        nyquist = 0.5 * taxa_amostragem
        corte_norm = freq_corte / nyquist
        b = signal.firwin(101, corte_norm, window='hamming')
        return signal.fftconvolve(sinal, b, mode='same')

class Visualizacao:
    @staticmethod
    def plotar_sinal(t, sinal, titulo='Sinal', downsample=1000):
        if len(t) > downsample:
            idx = np.linspace(0, len(t)-1, downsample).astype(int)
            t_plot = t[idx]
            sinal_plot = sinal[idx]
        else:
            t_plot, sinal_plot = t, sinal
        
        plt.figure(figsize=(10,4))
        plt.plot(t_plot, sinal_plot)
        plt.title(titulo)
        plt.xlabel('Tempo (s)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plotar_espectro(freq, espectro, titulo='Espectro'):
        plt.figure(figsize=(10,4))
        plt.plot(fftshift(freq), fftshift(espectro))
        plt.title(titulo)
        plt.xlabel('Frequência (Hz)')
        plt.ylabel('Magnitude (dB)')
        plt.yscale('log')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Teste de performance
    fs = 1e6
    t = np.linspace(0, 1, int(fs))
    sinal = np.sin(2*np.pi*1e5*t) + 0.5*np.sin(2*np.pi*3e5*t)
    
    # Análise de Fourier
    freq, espectro = Transformadas.fourier(sinal, t)
    Visualizacao.plotar_espectro(freq, espectro)
    
    # Modulação QPSK
    bits = np.random.randint(0, 2, 1000000)
    sinal_qpsk, _ = ModulacaoDigital.qpsk(bits)
    
    # Codificação Hamming
    codificador = CodificacaoCanal()
    dados_codificados = codificador.codificar_hamming(bits)
