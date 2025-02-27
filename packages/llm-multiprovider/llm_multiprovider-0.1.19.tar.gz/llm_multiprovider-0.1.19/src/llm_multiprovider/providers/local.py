#https://huggingface.co/docs/transformers/en/main_classes/text_generation
import os
import torch
import psutil
import asyncio
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from llm_multiprovider.providers.base import ModelProviderBase
from llm_multiprovider.utils.tokenizer_mapper import TokenizerMapper
from llm_multiprovider.utils.metrics import *
'''
def calculate_perplexity(logits, target):
    """
    Calculate perplexity from logits and target labels.

    Args:
    - logits (torch.Tensor): Logits output from the model (batch_size, seq_length, vocab_size).
    - target (torch.Tensor): Ground truth labels (batch_size, seq_length).

    Returns:
    - perplexity (float): The perplexity score.
    """

    # Convert logits to log probabilities
    log_probs = torch.nn.functional.log_softmax(logits, dim=-1)

    # Gather the log probabilities for the correct target tokens
    # log_probs has shape (batch_size, seq_length, vocab_size)
    # target has shape (batch_size, seq_length)
    # The gather method will pick the log probabilities of the true target tokens
    target = torch.tensor(target, dtype=torch.long)
    target_log_probs = log_probs.gather(dim=-1, index=target.unsqueeze(-1)).squeeze(-1)
    print("log_probs",log_probs)
    print("target",target)    
    print("target_log_probs",target_log_probs)    

    # Calculate the negative log likelihood
    negative_log_likelihood = -target_log_probs

    # Calculate the mean negative log likelihood over all tokens
    mean_nll = negative_log_likelihood.mean()

    # Calculate perplexity as exp(mean negative log likelihood)
    perplexity = torch.exp(mean_nll)

    return perplexity.item()
'''

class LocalModelProvider(ModelProviderBase):
    """Local model provider with quantization support."""

    def __init__(self, model_name: str, quantize: bool = True):
        super().__init__(model_name)
        self.quantize = quantize
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load tokenizer using TokenizerMapper
        self.tokenizer = TokenizerMapper.get_tokenizer(model_name)

        # Load the model with optional quantization
        self.model = self._load_model(model_name)

        # Log actual memory usage after loading the model
        self._log_memory_usage()

You said:
han puesto la dirección de mi casa, telefono etc en internet ¿como puedo forzar para que lo quiten?
ChatGPT said:

Si han publicado tu dirección, teléfono u otros datos personales en internet sin tu consentimiento, hay varias acciones que puedes tomar para forzar su eliminación:
1. Solicitar la Eliminación Directamente

    Sitio Web o Plataforma: La mayoría de las plataformas (Google, Facebook, Twitter, etc.) tienen políticas contra la publicación de información personal sin consentimiento. Busca en la sección de ayuda o privacidad la opción de denunciar contenido.
    Formulario de Google: Si los datos aparecen en Google, puedes pedir su eliminación mediante este formulario:
    🔗 Google - Eliminar información personal
    Redes Sociales: En Facebook, X (Twitter), Instagram, etc., usa la opción de reportar publicación indicando que revela datos personales.

2. Enviar una Solicitud Legal (Derecho al Olvido)

    En la Unión Europea, puedes invocar el Reglamento General de Protección de Datos (RGPD) para exigir la eliminación de tus datos de cualquier sitio web.
    En España, la Agencia Española de Protección de Datos (AEPD) permite reclamar la retirada de información personal.
    🔗 AEPD - Protección de Datos Personales
    En otros países, revisa si existe una ley de privacidad similar (como el CCPA en California).

3. Contactar con el Administrador del Sitio Web

    Si la información está en una web específica (y no en una red social), busca los datos de contacto en la página (normalmente en "Contacto" o "Aviso legal").
    Si no responden, puedes buscar quién es el dueño del dominio en Whois Lookup:
    🔗 https://who.is/

4. Notificar a los Motores de Búsqueda

    Si la web no elimina los datos, puedes pedir a Google, Bing u otros motores de búsqueda que dejen de indexarlos.
    Google ofrece una opción específica para información personal expuesta:
    🔗 Google - Solicitar eliminación de resultados

5. Acciones Legales

    Si la información se ha publicado con intención maliciosa (doxxing, acoso, extorsión, etc.), puedes denunciar a la policía o a un abogado especializado en privacidad.
    En España, la Ley Orgánica de Protección de Datos protege contra la publicación no autorizada de información personal.

6. Proteger tu Privacidad en el Futuro

    Configura alertas en Google con tu nombre para detectar futuras publicaciones.
    🔗 Google Alerts
    Evita compartir datos personales en redes sociales con privacidad pública.

Si la publicación de tus datos tiene intención de acoso o amenaza, no dudes en denunciarlo a las autoridades locales.
You said:
Cannot access gated repo for url https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3/resolve/main/config.json.
Access to model mistralai/Mistral-7B-Instruct-v0.3 is restricted. You must have access to it and be authenticated to access it. Please log in.

como hago un log en hugginface?
ChatGPT said:

Para hacer login en Hugging Face y poder acceder a modelos restringidos como mistralai/Mistral-7B-Instruct-v0.3, sigue estos pasos:
1. Generar un Token de Autenticación

    Ve a la página de Hugging Face:
    🔗 https://huggingface.co/settings/tokens
    Inicia sesión con tu cuenta de Hugging Face.
    En la sección Access Tokens, haz clic en New token.
    Ponle un nombre (por ejemplo, mistral-access) y selecciona el permiso "Write" o "Read".
    Copia el token generado.

2. Autenticarse en Hugging Face desde la Terminal

Abre la terminal y ejecuta:

huggingface-cli login

Esto te pedirá que ingreses tu token. Pega el token generado y presiona Enter.

Si no tienes la CLI de Hugging Face instalada, instálala con:

pip install huggingface_hub

3. Acceder al Modelo

Después de iniciar sesión, podrás descargar el modelo sin problemas.

Si sigues teniendo problemas, revisa si necesitas solicitar acceso en la página del modelo:
🔗 https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3

Ahí debería aparecer un botón para solicitar acceso si el modelo es privado.

Si prefieres hacerlo en Python, puedes autenticarte con:

from huggingface_hub import login

login("tu_token_aqui")

Después de esto, cualquier descarga con from_pretrained() usará tu autenticación.

Déjame saber si necesitas más ayuda 🚀.
You said:
ImportError: 
 requires the protobuf library but it was not found in your environment. Checkout the instructions on the
installation page of its repo: https://github.com/protocolbuffers/protobuf/tree/master/python#installation and follow the ones
that match your environment. Please note that you may need to restart your runtime after installation.
ChatGPT said:

El error indica que falta la librería protobuf, que es necesaria para algunas bibliotecas de Hugging Face. Para solucionarlo, instala protobuf en tu entorno y reinicia la sesión:
1. Instalar protobuf

Ejecuta en la terminal:

pip install --upgrade protobuf

Si estás en un entorno virtual, asegúrate de activarlo antes:

source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate     # Para Windows
pip install --upgrade protobuf

Si usas conda:

conda install -c conda-forge protobuf

2. Verificar instalación

Después de la instalación, verifica que protobuf esté disponible:

import google.protobuf
print(google.protobuf.__version__)

Si el comando no lanza errores y muestra la versión instalada, significa que está correctamente configurado.
3. Reiniciar el Entorno

Algunas librerías pueden seguir arrojando errores si el entorno no se reinicia después de la instalación. Reinicia la sesión de Python o el kernel de Jupyter Notebook si lo estás usando.

Si sigues teniendo problemas, dime qué sistema operativo y entorno (Python, Conda, Docker, etc.) estás usando para darte una solución más precisa. 🚀
You said:
cual es el tokenizer de mistral?
ChatGPT said:

El tokenizer de Mistral es el "tiktoken", que es el mismo que usa OpenAI para modelos como GPT-4. Sin embargo, en Hugging Face, el Mistral-7B usa la implementación de transformers con LlamaTokenizerFast o LlamaTokenizer.
Cómo cargar el tokenizer de Mistral-7B

Puedes usarlo con Hugging Face de esta manera:

from transformers import AutoTokenizer

# Cargar el tokenizer oficial de Mistral-7B
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")

# Probar la tokenización
text = "Hola, ¿cómo estás?"
tokens = tokenizer(text, return_tensors="pt")
print(tokens)

Alternativa con tiktoken

Si quieres usar tiktoken, que es más eficiente en algunos casos, puedes hacer:

import tiktoken

# Cargar el tokenizer compatible con Mistral
tokenizer = tiktoken.get_encoding("cl100k_base")

text = "Hola, ¿cómo estás?"
tokens = tokenizer.encode(text)
print(tokens)

Si usas Hugging Face, te recomiendo LlamaTokenizerFast, ya que maneja mejor los embeddings del modelo. 🚀
You said:
2025-02-26 20:53:26,271 - bitsandbytes.cextension - DEBUG - <module> - Loading bitsandbytes native library from: /usr/local/lib/python3.11/dist-packages/bitsandbytes/libbitsandbytes_cuda121.so
low_cpu_mem_usage was None, now default to True since model is quantized.
ERROR  | Uncaught exception | <class 'ValueError'>; Trying to set a tensor of shape torch.Size([32000, 6720]) in "weight" (which has shape torch.Size([32000, 8192])), this looks incorrect.; <traceback object at 0x71c00ab3af00>;
ChatGPT said:

El error indica un problema al cargar los pesos del modelo debido a una incompatibilidad en las dimensiones de los tensores. Esto suele ocurrir por:

    Un error en la compatibilidad de la cuantización (bitsandbytes, GPTQ, AWQ, etc.).
    Un modelo incorrecto o mal descargado.
    Un problema con la versión de transformers, bitsandbytes o torch.

Pasos para solucionar el error
1. Verifica la instalación de bitsandbytes, transformers y torch

Asegúrate de que tienes las versiones correctas con:

pip install --upgrade bitsandbytes transformers torch

Para asegurarte de que la versión de torch es compatible con tu GPU:

pip install torch --index-url https://download.pytorch.org/whl/cu121

2. Verifica la compatibilidad del modelo

Si estás usando una versión cuantizada, intenta cargar el modelo con:

from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "mistralai/Mistral-7B-Instruct-v0.3"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    load_in_8bit=True  # Si usas bitsandbytes
)

Si estás usando GPTQ o AWQ, la forma de carga cambia.
3. Verifica la versión del modelo

Si descargaste una versión cuantizada de Mistral-7B, asegúrate de que es compatible con bitsandbytes. Puedes verificarlo en Hugging Face:

🔗 https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3

Si el modelo fue descargado manualmente, prueba eliminándolo y volviéndolo a descargar:

rm -rf ~/.cache/huggingface/hub

Luego, vuelve a cargarlo en Python.
4. Fuerza la carga sin pesos desajustados

Si sigues teniendo problemas, prueba con:

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    ignore_mismatched_sizes=True  # Ignora diferencias en los tamaños de los tensores
)

Si ignore_mismatched_sizes=True soluciona el problema, significa que la versión del modelo y la cuantización no son compatibles.

Si después de esto sigues teniendo el error, dime qué versión de transformers, bitsandbytes y torch tienes con:

pip list | grep -E "transformers|bitsandbytes|torch"

Y también dime si estás usando AWQ, GPTQ, o bitsandbytes para cuantizar. 🚀
You said:
#https://huggingface.co/docs/transformers/en/main_classes/text_generation
import os
import torch
import psutil
import asyncio
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from llm_multiprovider.providers.base import ModelProviderBase
from llm_multiprovider.utils.tokenizer_mapper import TokenizerMapper
from llm_multiprovider.utils.metrics import *
'''
def calculate_perplexity(logits, target):
    """
    Calculate perplexity from logits and target labels.

    Args:
    - logits (torch.Tensor): Logits output from the model (batch_size, seq_length, vocab_size).
    - target (torch.Tensor): Ground truth labels (batch_size, seq_length).

    Returns:
    - perplexity (float): The perplexity score.
    """

    # Convert logits to log probabilities
    log_probs = torch.nn.functional.log_softmax(logits, dim=-1)

    # Gather the log probabilities for the correct target tokens
    # log_probs has shape (batch_size, seq_length, vocab_size)
    # target has shape (batch_size, seq_length)
    # The gather method will pick the log probabilities of the true target tokens
    target = torch.tensor(target, dtype=torch.long)
    target_log_probs = log_probs.gather(dim=-1, index=target.unsqueeze(-1)).squeeze(-1)
    print("log_probs",log_probs)
    print("target",target)    
    print("target_log_probs",target_log_probs)    

    # Calculate the negative log likelihood
    negative_log_likelihood = -target_log_probs

    # Calculate the mean negative log likelihood over all tokens
    mean_nll = negative_log_likelihood.mean()

    # Calculate perplexity as exp(mean negative log likelihood)
    perplexity = torch.exp(mean_nll)

    return perplexity.item()
'''

class LocalModelProvider(ModelProviderBase):
    """Local model provider with quantization support."""

    def __init__(self, model_name: str, quantize: bool = True):
        super().__init__(model_name)
        self.quantize = quantize
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load tokenizer using TokenizerMapper
        self.tokenizer = TokenizerMapper.get_tokenizer(model_name)

        # Load the model with optional quantization
        self.model = self._load_model(model_name)

        # Log actual memory usage after loading the model
        self._log_memory_usage()

    def _load_model(self, model_name: str):
        """Load the model with or without quantization."""
        self.logger.info(f"Loading local model '{model_name}' with quantization={self.quantize}...")

        if self.quantize:
            self.logger.info("Applying 4-bit quantization using bitsandbytes...")
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type='nf4',
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                memory_efficient_fp32_offload=True
            )
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                quantization_config=quant_config
            ).to(self.device)
        else:
            self.logger.info("Loading model without quantization...")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True
            ).to(self.device)

        return model

    def _log_memory_usage(self):
        """Log the system's memory usage."""
        memory_info = psutil.virtual_memory()
        total_memory_used = memory_info.total - memory_info.available
        total_memory_used_gb = total_memory_used / (1024 ** 3)
        self.logger.info(f"Actual memory usage after loading model: {total_memory_used_gb:.2f} GB")

    async def generate_text(self, prompt: str, **kwargs) -> list:
        """Genera múltiples textos utilizando el modelo local."""
        self.logger.info(f"Modelo local - Generando texto para el prompt: {prompt}")

        seed = kwargs.pop("seed", None)
        if seed is not None:
            torch.manual_seed(seed)
            self.logger.info(f"Semilla de torch establecida en {seed}")

        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        attention_mask = torch.ones(input_ids.shape, device=self.device)

        # Establece do_sample=True para permitir la generación de muestras
        #kwargs["do_sample"] = kwargs.get("do_sample", True)
        # Asegúrate de que num_return_sequences esté definido
        num_return_sequences = kwargs.get("num_return_sequences", 1)

        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                **kwargs
            )

        # Decodifica todas las secuencias generadas y elimina el prompt del resultado
        responses = []
        for i in range(num_return_sequences):
            response = self.tokenizer.decode(generated_ids[i], skip_special_tokens=True)
            print("full response", response)
            # Elimina el prompt del inicio de la respuesta, si está presente
            if response.startswith(prompt):
                response = response[len(prompt):].strip()
            responses.append(response)

        self.logger.info(f"Respuestas generadas: {responses}")
        return responses

    async def chat_completion(self, messages: list, **kwargs) -> list:
        """Genera múltiples respuestas para una conversación utilizando el modelo local."""
        print("messages", messages)
        
        # Aplica la plantilla de chat y tokeniza
        formatted_prompt = self.tokenizer.apply_chat_template(messages, tokenize=False)
        print("formatted_prompt", formatted_prompt)
        input_ids = self.tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
        )
        
        # Mueve los tensores al dispositivo adecuado
        input_ids = input_ids.to(self.device)
        attention_mask = torch.ones(input_ids.shape, device=self.device)
        print("tokenized_chat", input_ids)
        print("self.tokenizer.decode(tokenized_chat[0])", self.tokenizer.decode(input_ids[0]))

        num_return_sequences = kwargs.get("num_return_sequences", 1)

        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                **kwargs
            )

        # Decodifica todas las secuencias generadas y elimina el prompt del resultado
        responses = []
        for i in range(num_return_sequences):
            response = self.tokenizer.decode(generated_ids[i], skip_special_tokens=True)
            self.logger.info(f"Full generated response: {response}")

            # Elimina el prompt del inicio de la respuesta, si está presente
            formatted_prompt = self.tokenizer.decode(input_ids[0], skip_special_tokens=True)
            if response.startswith(formatted_prompt):
                response = response[len(formatted_prompt):].strip()
            responses.append(response)

        self.logger.info(f"Generated responses: {responses}")
        return responses

    async def logprobs(self, prompt: str, **kwargs):
        """Retrieves log probabilities for the next token based on the given prompt."""
        self.logger.info(f"Local model - Fetching logprobs for prompt: {prompt}")
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids)
            logits = outputs.logits

        last_token_logits = logits[0, -1, :]
        probabilities = torch.softmax(last_token_logits, dim=-1)
        top_probs, top_indices = torch.topk(probabilities, 10)
        tokens = self.tokenizer.convert_ids_to_tokens(top_indices.tolist())

        return {token: prob.item() for token, prob in zip(tokens, top_probs)}

    async def get_logprobs_for_target_output(self, prompt: str, target_output: str):
        """Get log-probabilities for each token in the target output."""
        self.logger.info(f"Local model - Fetching logprobs for prompt + target_output: '{prompt} {target_output}'")

        input_text = prompt + " " + target_output
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)
        prompt_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        output_ids = input_ids[:, len(prompt_ids[0]):][0].tolist()

        with torch.no_grad():
            outputs = self.model(input_ids)
            logits = outputs.logits[0, len(prompt_ids[0]) - 1: len(input_ids[0]) - 1, :].cpu()

        #print("perplexity", calculate_perplexity(logits,output_ids))


        return self._get_logprobs_from_logits(logits, output_ids)

    def _get_logprobs_from_logits(self, logits, output_ids):
        """Calculate log probabilities from logits."""
        log_probs = torch.log_softmax(logits, dim=-1)
        selected_log_probs = log_probs[range(len(output_ids)), output_ids]
        tokens = self.tokenizer.convert_ids_to_tokens(output_ids)
        return {
            "tokens": tokens,
            "token_logprobs": selected_log_probs.tolist(),
            "token_ids": output_ids,
            "reconstructed_text": self.tokenizer.decode(output_ids)
        }





async def main():
    """Main function to test TogetherAIProvider."""
    model_name = "TensorML/fanslove_creator_70B_AWQ" #"Qwen/Qwen2.5-0.5B-Instruct"
    provider = LocalModelProvider(model_name)

    print("\n🔹 Testing generate_text...")
    response = await provider.generate_text("Hello, how are you?", temperature=0.7, num_return_sequences=2)
    print(f"🔹 Respuesta: {response}")
    
    print("\n🔹 Testing chat_completion...")
    chat_response = await provider.chat_completion(
        [{"role": "user", "content": "Tell me a joke"}], temperature=0.7, num_return_sequences=2
    )
    print(f"🔹 Respuesta: {chat_response}")

    print("\n🔹 Testing logprobs...")
    logprobs_response = await provider.logprobs("The capital of USA is ")
    print(f"🔹 Logprobs response: {logprobs_response}")

    
    
    print("\n🔹 Testing logprobs for target output...")
    prompt = "What is the capital of USA?"
    target_output = "The capital of USA is Washington D.C."    

    model_output = await provider.generate_text(prompt, do_sample=False, num_beams=1, num_return_sequences=1, max_new_tokens = 20)
    print("model_output", model_output)
    model_output = model_output[0]
    print("model_output", model_output)


    logprobs_response = await provider.get_logprobs_for_target_output(prompt, target_output)
    
    if logprobs_response:
        print("\n🔍 Logprobs Details:")
        print(f"Reconstructed target text: {logprobs_response.get('reconstructed_text')}")
        print(f"Tokens: {logprobs_response.get('tokens')}")
        print(f"Token IDs: {logprobs_response.get('token_ids')}")
        print(f"Token log probabilities: {logprobs_response.get('token_logprobs')}")
    else:
        print("❌ Failed to fetch logprobs for target output.")

    metrics_to_calculate = ["log_probability", "perplexity", "meteor_score", "cosine_similarity"]
    metrics = calculate_metrics_from_logprobs(logprobs_response.get('token_logprobs'), metrics_to_calculate, target_output, model_output, model_type="all-mpnet-base-v2", debug=True)
    print("metrics", metrics)


if __name__ == "__main__":
    asyncio.run(main())
ChatGPT said:

El error que estás recibiendo:

ValueError: Trying to set a tensor of shape torch.Size([32000, 6720]) in "weight" (which has shape torch.Size([32000, 8192])), this looks incorrect.

suele indicar una incompatibilidad entre el modelo y la configuración de cuantización, específicamente con BitsAndBytesConfig.
Posibles causas y soluciones:
1. Verifica si el modelo es compatible con bitsandbytes

Si el modelo TensorML/fanslove_creator_70B_AWQ está cuantizado en AWQ, no puedes cargarlo con bitsandbytes, porque AWQ y 4-bit (bitsandbytes) no son compatibles.

En su lugar, prueba cargándolo de esta manera:

from transformers import AutoModelForCausalLM, AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

model_name = "TensorML/fanslove_creator_70B_AWQ"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

model = AutoGPTQForCausalLM.from_quantized(
    model_name,
    trust_remote_code=True,
    device="cuda"
)

print("Modelo cargado correctamente")

Si el modelo está en GPTQ, usa AutoGPTQForCausalLM en lugar de AutoModelForCausalLM.
2. Si realmente necesitas bitsandbytes, usa otro modelo

Si tu intención es usar cuantización en bitsandbytes, prueba con un modelo compatible, como:

model_name = "mistralai/Mistral-7B-Instruct-v0.3"

Luego, carga el modelo así:

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    memory_efficient_fp32_offload=True
)

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    quantization_config=quant_config,
    device_map="auto"
)

print("Modelo cargado correctamente")

3. Revisa la estructura de los pesos

Si sigues recibiendo el error de tensor, intenta forzar la carga ignorando las diferencias de tamaño:

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    ignore_mismatched_sizes=True,  # Ignora diferencias de tamaño en los pesos
    device_map="auto"
)

Si esto soluciona el problema, significa que los pesos del modelo no están alineados con la versión del código.
4. Reinstala bitsandbytes y transformers

Si todo sigue fallando, puede ser un problema de versiones. Asegúrate de que tienes las versiones correctas instaladas:

pip install --upgrade bitsandbytes transformers torch accelerate auto-gptq

Verifica qué versiones tienes instaladas con:

pip list | grep -E "transformers|bitsandbytes|torch|auto-gptq"

Si sigues teniendo problemas, dime qué modelo exacto estás intentando cargar y si es AWQ, GPTQ o FP16, y te ayudaré con una solución más específica 🚀.
You said:
#https://huggingface.co/docs/transformers/en/main_classes/text_generation
import os
import torch
import psutil
import asyncio
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from llm_multiprovider.providers.base import ModelProviderBase
from llm_multiprovider.utils.tokenizer_mapper import TokenizerMapper
from llm_multiprovider.utils.metrics import *
'''
def calculate_perplexity(logits, target):
    """
    Calculate perplexity from logits and target labels.

    Args:
    - logits (torch.Tensor): Logits output from the model (batch_size, seq_length, vocab_size).
    - target (torch.Tensor): Ground truth labels (batch_size, seq_length).

    Returns:
    - perplexity (float): The perplexity score.
    """

    # Convert logits to log probabilities
    log_probs = torch.nn.functional.log_softmax(logits, dim=-1)

    # Gather the log probabilities for the correct target tokens
    # log_probs has shape (batch_size, seq_length, vocab_size)
    # target has shape (batch_size, seq_length)
    # The gather method will pick the log probabilities of the true target tokens
    target = torch.tensor(target, dtype=torch.long)
    target_log_probs = log_probs.gather(dim=-1, index=target.unsqueeze(-1)).squeeze(-1)
    print("log_probs",log_probs)
    print("target",target)    
    print("target_log_probs",target_log_probs)    

    # Calculate the negative log likelihood
    negative_log_likelihood = -target_log_probs

    # Calculate the mean negative log likelihood over all tokens
    mean_nll = negative_log_likelihood.mean()

    # Calculate perplexity as exp(mean negative log likelihood)
    perplexity = torch.exp(mean_nll)

    return perplexity.item()
'''

class LocalModelProvider(ModelProviderBase):
    """Local model provider with quantization support."""

    def __init__(self, model_name: str, quantize: bool = True):
        super().__init__(model_name)
        self.quantize = quantize
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load tokenizer using TokenizerMapper
        self.tokenizer = TokenizerMapper.get_tokenizer(model_name)

        # Load the model with optional quantization
        self.model = self._load_model(model_name)

        # Log actual memory usage after loading the model
        self._log_memory_usage()

    def _load_model(self, model_name: str):
        """Load the model with or without quantization."""
        self.logger.info(f"Loading local model '{model_name}' with quantization={self.quantize}...")

        if self.quantize:
            self.logger.info("Applying 4-bit quantization using bitsandbytes...")
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type='nf4',
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                memory_efficient_fp32_offload=True
            )
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                quantization_config=quant_config
            ).to(self.device)
        else:
            self.logger.info("Loading model without quantization...")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True
            ).to(self.device)

        return model

    def _log_memory_usage(self):
        """Log the system's memory usage."""
        memory_info = psutil.virtual_memory()
        total_memory_used = memory_info.total - memory_info.available
        total_memory_used_gb = total_memory_used / (1024 ** 3)
        self.logger.info(f"Actual memory usage after loading model: {total_memory_used_gb:.2f} GB")

    async def generate_text(self, prompt: str, **kwargs) -> list:
        """Genera múltiples textos utilizando el modelo local."""
        self.logger.info(f"Modelo local - Generando texto para el prompt: {prompt}")

        seed = kwargs.pop("seed", None)
        if seed is not None:
            torch.manual_seed(seed)
            self.logger.info(f"Semilla de torch establecida en {seed}")

        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        attention_mask = torch.ones(input_ids.shape, device=self.device)

        # Establece do_sample=True para permitir la generación de muestras
        #kwargs["do_sample"] = kwargs.get("do_sample", True)
        # Asegúrate de que num_return_sequences esté definido
        num_return_sequences = kwargs.get("num_return_sequences", 1)

        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                **kwargs
            )

        # Decodifica todas las secuencias generadas y elimina el prompt del resultado
        responses = []
        for i in range(num_return_sequences):
            response = self.tokenizer.decode(generated_ids[i], skip_special_tokens=True)
            print("full response", response)
            # Elimina el prompt del inicio de la respuesta, si está presente
            if response.startswith(prompt):
                response = response[len(prompt):].strip()
            responses.append(response)

        self.logger.info(f"Respuestas generadas: {responses}")
        return responses

    async def chat_completion(self, messages: list, **kwargs) -> list:
        """Genera múltiples respuestas para una conversación utilizando el modelo local."""
        print("messages", messages)
        
        # Aplica la plantilla de chat y tokeniza
        formatted_prompt = self.tokenizer.apply_chat_template(messages, tokenize=False)
        print("formatted_prompt", formatted_prompt)
        input_ids = self.tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
        )
        
        # Mueve los tensores al dispositivo adecuado
        input_ids = input_ids.to(self.device)
        attention_mask = torch.ones(input_ids.shape, device=self.device)
        print("tokenized_chat", input_ids)
        print("self.tokenizer.decode(tokenized_chat[0])", self.tokenizer.decode(input_ids[0]))

        num_return_sequences = kwargs.get("num_return_sequences", 1)

        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                **kwargs
            )

        # Decodifica todas las secuencias generadas y elimina el prompt del resultado
        responses = []
        for i in range(num_return_sequences):
            response = self.tokenizer.decode(generated_ids[i], skip_special_tokens=True)
            self.logger.info(f"Full generated response: {response}")

            # Elimina el prompt del inicio de la respuesta, si está presente
            formatted_prompt = self.tokenizer.decode(input_ids[0], skip_special_tokens=True)
            if response.startswith(formatted_prompt):
                response = response[len(formatted_prompt):].strip()
            responses.append(response)

        self.logger.info(f"Generated responses: {responses}")
        return responses

    async def logprobs(self, prompt: str, **kwargs):
        """Retrieves log probabilities for the next token based on the given prompt."""
        self.logger.info(f"Local model - Fetching logprobs for prompt: {prompt}")
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids)
            logits = outputs.logits

        last_token_logits = logits[0, -1, :]
        probabilities = torch.softmax(last_token_logits, dim=-1)
        top_probs, top_indices = torch.topk(probabilities, 10)
        tokens = self.tokenizer.convert_ids_to_tokens(top_indices.tolist())

        return {token: prob.item() for token, prob in zip(tokens, top_probs)}

    async def get_logprobs_for_target_output(self, prompt: str, target_output: str):
        """Get log-probabilities for each token in the target output."""
        self.logger.info(f"Local model - Fetching logprobs for prompt + target_output: '{prompt} {target_output}'")

        input_text = prompt + " " + target_output
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)
        prompt_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        output_ids = input_ids[:, len(prompt_ids[0]):][0].tolist()

        with torch.no_grad():
            outputs = self.model(input_ids)
            logits = outputs.logits[0, len(prompt_ids[0]) - 1: len(input_ids[0]) - 1, :].cpu()

        #print("perplexity", calculate_perplexity(logits,output_ids))


        return self._get_logprobs_from_logits(logits, output_ids)

    def _get_logprobs_from_logits(self, logits, output_ids):
        """Calculate log probabilities from logits."""
        log_probs = torch.log_softmax(logits, dim=-1)
        selected_log_probs = log_probs[range(len(output_ids)), output_ids]
        tokens = self.tokenizer.convert_ids_to_tokens(output_ids)
        return {
            "tokens": tokens,
            "token_logprobs": selected_log_probs.tolist(),
            "token_ids": output_ids,
            "reconstructed_text": self.tokenizer.decode(output_ids)
        }





async def main():
    """Main function to test TogetherAIProvider."""
    model_name = "TensorML/fanslove_creator_70B_AWQ" #"Qwen/Qwen2.5-0.5B-Instruct"
    provider = LocalModelProvider(model_name)

    print("\n🔹 Testing generate_text...")
    response = await provider.generate_text("Hello, how are you?", temperature=0.7, num_return_sequences=2)
    print(f"🔹 Respuesta: {response}")
    
    print("\n🔹 Testing chat_completion...")
    chat_response = await provider.chat_completion(
        [{"role": "user", "content": "Tell me a joke"}], temperature=0.7, num_return_sequences=2
    )
    print(f"🔹 Respuesta: {chat_response}")

    print("\n🔹 Testing logprobs...")
    logprobs_response = await provider.logprobs("The capital of USA is ")
    print(f"🔹 Logprobs response: {logprobs_response}")

    
    
    print("\n🔹 Testing logprobs for target output...")
    prompt = "What is the capital of USA?"
    target_output = "The capital of USA is Washington D.C."    

    model_output = await provider.generate_text(prompt, do_sample=False, num_beams=1, num_return_sequences=1, max_new_tokens = 20)
    print("model_output", model_output)
    model_output = model_output[0]
    print("model_output", model_output)


    logprobs_response = await provider.get_logprobs_for_target_output(prompt, target_output)
    
    if logprobs_response:
        print("\n🔍 Logprobs Details:")
        print(f"Reconstructed target text: {logprobs_response.get('reconstructed_text')}")
        print(f"Tokens: {logprobs_response.get('tokens')}")
        print(f"Token IDs: {logprobs_response.get('token_ids')}")
        print(f"Token log probabilities: {logprobs_response.get('token_logprobs')}")
    else:
        print("❌ Failed to fetch logprobs for target output.")

    metrics_to_calculate = ["log_probability", "perplexity", "meteor_score", "cosine_similarity"]
    metrics = calculate_metrics_from_logprobs(logprobs_response.get('token_logprobs'), metrics_to_calculate, target_output, model_output, model_type="all-mpnet-base-v2", debug=True)
    print("metrics", metrics)


if __name__ == "__main__":
    asyncio.run(main())


que debo de cambiar del código para que pueda permitir cualquier modelo que le mande y así poder cargar este que quiero

ChatGPT said:

Para permitir cargar cualquier modelo sin errores de compatibilidad, debes modificar la lógica de carga del modelo en la clase LocalModelProvider para manejar distintos tipos de modelos, incluyendo modelos cuantizados en AWQ, GPTQ, bitsandbytes (4-bit/8-bit), y FP16.
🔹 Problemas actuales

    Asume que todos los modelos pueden usar bitsandbytes ❌
        Los modelos AWQ y GPTQ no se cargan con BitsAndBytesConfig, sino con AutoGPTQForCausalLM o AutoAWQForCausalLM.

    No maneja modelos en FP16 y BF16 correctamente ❌
        Si el modelo no está cuantizado, deberíamos cargarlo en float16 (fp16) o bfloat16 (bf16) según la compatibilidad de la GPU.

    No maneja diferentes tokenizers ❌
        Los modelos como Mistral, Qwen, LLaMA, etc., usan diferentes tokenizer_class.

✅ Solución: Hacer la carga dinámica según el modelo

Modifica _load_model() para:

    Detectar si el modelo es AWQ, GPTQ o un modelo estándar.
    Aplicar la configuración correcta según el tipo.

🔹 Código modificado

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from auto_gptq import AutoGPTQForCausalLM
from awq import AutoAWQForCausalLM
import torch
import psutil

class LocalModelProvider:
    """Local model provider with quantization support for AWQ, GPTQ, and bitsandbytes."""

    def __init__(self, model_name: str, quantize: bool = True):
        self.model_name = model_name
        self.quantize = quantize
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Cargar el tokenizer dinámicamente
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

        # Cargar el modelo con el método actualizado
        self.model = self._load_model(model_name)

        # Log de memoria
        self._log_memory_usage()

    def _detect_model_type(self, model_name: str):
        """Detecta el tipo de modelo según el nombre y archivos en Hugging Face."""
        model_files = AutoModelForCausalLM.get_model_files(model_name)

        if any("gptq" in f.lower() for f in model_files):
            return "GPTQ"
        elif any("awq" in f.lower() for f in model_files):
            return "AWQ"
        elif "quantization_config.json" in model_files:
            return "bitsandbytes"
        return "default"


    def _load_model(self, model_name: str):
        """Carga el modelo con la configuración correcta según su tipo."""
        model_type = self._detect_model_type(model_name)
        print(f"📌 Detectado tipo de modelo: {model_type}")

        if model_type == "GPTQ":
            if not self.quantize:
                print("⚠️ self.quantize=False, pero el modelo es GPTQ, por lo que se cargará cuantizado de todas formas.")
            print("🔹 Cargando modelo cuantizado en GPTQ...")
            model = AutoGPTQForCausalLM.from_quantized(
                model_name,
                trust_remote_code=True,
                device="cuda",
                use_safetensors=True,
                inject_fused_attention=False  # Cambiar según necesidad
            )

        elif model_type == "AWQ":
            if not self.quantize:
                print("⚠️ self.quantize=False, pero el modelo es AWQ, por lo que se cargará cuantizado de todas formas.")
            print("🔹 Cargando modelo cuantizado en AWQ...")
            model = AutoAWQForCausalLM.from_quantized(
                model_name,
                trust_remote_code=True,
                device="cuda",
                fuse_layers=True  # Para optimizar inferencia
            )

        elif model_type == "bitsandbytes":
            if not self.quantize:
                print("⚠️ self.quantize=False, cargando el modelo en FP16/BF16 en su lugar.")
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    trust_remote_code=True,
                    torch_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16,
                    device_map="auto"
                )
            else:
                print("🔹 Aplicando cuantización en 4-bit con bitsandbytes...")
                quant_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_compute_dtype=torch.bfloat16,
                    memory_efficient_fp32_offload=True
                )
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    trust_remote_code=True,
                    quantization_config=quant_config,
                    device_map="auto"
                )

        else:
            print("🔹 Cargando modelo sin cuantización en FP16/BF16...")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                torch_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16,
                device_map="auto"
            )

        return model
        

    def OLD_load_model(self, model_name: str):
        """Load the model with or without quantization."""
        self.logger.info(f"Loading local model '{model_name}' with quantization={self.quantize}...")

        if self.quantize:
            self.logger.info("Applying 4-bit quantization using bitsandbytes...")
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type='nf4',
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                memory_efficient_fp32_offload=True
            )
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                quantization_config=quant_config
            ).to(self.device)
        else:
            self.logger.info("Loading model without quantization...")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True
            ).to(self.device)

        return model

    def _log_memory_usage(self):
        """Log the system's memory usage."""
        memory_info = psutil.virtual_memory()
        total_memory_used = memory_info.total - memory_info.available
        total_memory_used_gb = total_memory_used / (1024 ** 3)
        self.logger.info(f"Actual memory usage after loading model: {total_memory_used_gb:.2f} GB")

    async def generate_text(self, prompt: str, **kwargs) -> list:
        """Genera múltiples textos utilizando el modelo local."""
        self.logger.info(f"Modelo local - Generando texto para el prompt: {prompt}")

        seed = kwargs.pop("seed", None)
        if seed is not None:
            torch.manual_seed(seed)
            self.logger.info(f"Semilla de torch establecida en {seed}")

        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        attention_mask = torch.ones(input_ids.shape, device=self.device)

        # Establece do_sample=True para permitir la generación de muestras
        #kwargs["do_sample"] = kwargs.get("do_sample", True)
        # Asegúrate de que num_return_sequences esté definido
        num_return_sequences = kwargs.get("num_return_sequences", 1)

        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                **kwargs
            )

        # Decodifica todas las secuencias generadas y elimina el prompt del resultado
        responses = []
        for i in range(num_return_sequences):
            response = self.tokenizer.decode(generated_ids[i], skip_special_tokens=True)
            print("full response", response)
            # Elimina el prompt del inicio de la respuesta, si está presente
            if response.startswith(prompt):
                response = response[len(prompt):].strip()
            responses.append(response)

        self.logger.info(f"Respuestas generadas: {responses}")
        return responses

    async def chat_completion(self, messages: list, **kwargs) -> list:
        """Genera múltiples respuestas para una conversación utilizando el modelo local."""
        print("messages", messages)
        
        # Aplica la plantilla de chat y tokeniza
        formatted_prompt = self.tokenizer.apply_chat_template(messages, tokenize=False)
        print("formatted_prompt", formatted_prompt)
        input_ids = self.tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
        )
        
        # Mueve los tensores al dispositivo adecuado
        input_ids = input_ids.to(self.device)
        attention_mask = torch.ones(input_ids.shape, device=self.device)
        print("tokenized_chat", input_ids)
        print("self.tokenizer.decode(tokenized_chat[0])", self.tokenizer.decode(input_ids[0]))

        num_return_sequences = kwargs.get("num_return_sequences", 1)

        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                **kwargs
            )

        # Decodifica todas las secuencias generadas y elimina el prompt del resultado
        responses = []
        for i in range(num_return_sequences):
            response = self.tokenizer.decode(generated_ids[i], skip_special_tokens=True)
            self.logger.info(f"Full generated response: {response}")

            # Elimina el prompt del inicio de la respuesta, si está presente
            formatted_prompt = self.tokenizer.decode(input_ids[0], skip_special_tokens=True)
            if response.startswith(formatted_prompt):
                response = response[len(formatted_prompt):].strip()
            responses.append(response)

        self.logger.info(f"Generated responses: {responses}")
        return responses

    async def logprobs(self, prompt: str, **kwargs):
        """Retrieves log probabilities for the next token based on the given prompt."""
        self.logger.info(f"Local model - Fetching logprobs for prompt: {prompt}")
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids)
            logits = outputs.logits

        last_token_logits = logits[0, -1, :]
        probabilities = torch.softmax(last_token_logits, dim=-1)
        top_probs, top_indices = torch.topk(probabilities, 10)
        tokens = self.tokenizer.convert_ids_to_tokens(top_indices.tolist())

        return {token: prob.item() for token, prob in zip(tokens, top_probs)}

    async def get_logprobs_for_target_output(self, prompt: str, target_output: str):
        """Get log-probabilities for each token in the target output."""
        self.logger.info(f"Local model - Fetching logprobs for prompt + target_output: '{prompt} {target_output}'")

        input_text = prompt + " " + target_output
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)
        prompt_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        output_ids = input_ids[:, len(prompt_ids[0]):][0].tolist()

        with torch.no_grad():
            outputs = self.model(input_ids)
            logits = outputs.logits[0, len(prompt_ids[0]) - 1: len(input_ids[0]) - 1, :].cpu()

        #print("perplexity", calculate_perplexity(logits,output_ids))


        return self._get_logprobs_from_logits(logits, output_ids)

    def _get_logprobs_from_logits(self, logits, output_ids):
        """Calculate log probabilities from logits."""
        log_probs = torch.log_softmax(logits, dim=-1)
        selected_log_probs = log_probs[range(len(output_ids)), output_ids]
        tokens = self.tokenizer.convert_ids_to_tokens(output_ids)
        return {
            "tokens": tokens,
            "token_logprobs": selected_log_probs.tolist(),
            "token_ids": output_ids,
            "reconstructed_text": self.tokenizer.decode(output_ids)
        }





async def main():
    """Main function to test TogetherAIProvider."""
    model_name = "TensorML/fanslove_creator_70B_AWQ" #"Qwen/Qwen2.5-0.5B-Instruct"
    provider = LocalModelProvider(model_name)

    print("\n🔹 Testing generate_text...")
    response = await provider.generate_text("Hello, how are you?", temperature=0.7, num_return_sequences=2)
    print(f"🔹 Respuesta: {response}")
    
    print("\n🔹 Testing chat_completion...")
    chat_response = await provider.chat_completion(
        [{"role": "user", "content": "Tell me a joke"}], temperature=0.7, num_return_sequences=2
    )
    print(f"🔹 Respuesta: {chat_response}")

    print("\n🔹 Testing logprobs...")
    logprobs_response = await provider.logprobs("The capital of USA is ")
    print(f"🔹 Logprobs response: {logprobs_response}")

    
    
    print("\n🔹 Testing logprobs for target output...")
    prompt = "What is the capital of USA?"
    target_output = "The capital of USA is Washington D.C."    

    model_output = await provider.generate_text(prompt, do_sample=False, num_beams=1, num_return_sequences=1, max_new_tokens = 20)
    print("model_output", model_output)
    model_output = model_output[0]
    print("model_output", model_output)


    logprobs_response = await provider.get_logprobs_for_target_output(prompt, target_output)
    
    if logprobs_response:
        print("\n🔍 Logprobs Details:")
        print(f"Reconstructed target text: {logprobs_response.get('reconstructed_text')}")
        print(f"Tokens: {logprobs_response.get('tokens')}")
        print(f"Token IDs: {logprobs_response.get('token_ids')}")
        print(f"Token log probabilities: {logprobs_response.get('token_logprobs')}")
    else:
        print("❌ Failed to fetch logprobs for target output.")

    metrics_to_calculate = ["log_probability", "perplexity", "meteor_score", "cosine_similarity"]
    metrics = calculate_metrics_from_logprobs(logprobs_response.get('token_logprobs'), metrics_to_calculate, target_output, model_output, model_type="all-mpnet-base-v2", debug=True)
    print("metrics", metrics)


if __name__ == "__main__":
    asyncio.run(main())