---
layout: post
title: Criando Jarbas
date: 2018-12-29
description: Como criar o Jarbas?
toc: true
---

# Limpezas de final de ano e e-mails

Conforme o fim do ano se aproxima, eu começo a fazer limpezas na minha vida. Desde jogar coisas fora e doar roupas até limpar com mais carinho minha caixa de e-mail e meus arquivos.

Nesse processo, notei que eu recebo alguns e-mails que tem sua utilidade atrelada à um prazo de validade. Quão bom é uma newsletter diária 48h depois? Quão útil é uma promoção "só para hoje" vista uma semana depois? Para tentar resolver esse problema, desenvolvi a ideia do Jarbas.

## Apresentando Jarbas

O Jarbas é um mordomo genérico. Sua função é simplesmente tentar identificar e-mails que não são úteis e tirá-los do meu caminho. Isso torna mais fácil que eu enxergue o que realmente importa na minha caixa de entrada. Como eu uso GMail, o Jarbas será voltado para ele.

### Buscas Avançadas no GMail

O GMail possui um sistema de busca que suporta bastante [operadores diferentes](https://support.google.com/mail/answer/7190?hl=pt-BR). Por exemplo, eu posso buscar todos os e-mails que possuem a palavra "imobiliária" e que foram recebidos entre o dia 10/11/2012 e o dia 11/12/2013 com a seguinte expressão:

```
imobiliária AND AFTER:2012-11-10 AND BEFORE:2013-12-11
```

Note que a data é escrita no formato ANO-MÊS-DIA. Isso vem da ISO 8601. Não vou entrar em detalhes sobre formatos de data, mas observe a semelhança entre essa maneira de escrever datas e a forma como escrevemos números no nosso dia-a-dia.

Para representar o número "mil duzentos e quarenta e três", começamos com o número de maior magnitude ― o milhar ― depois a centena, a dezena e por último a unidade - 1243.

O formato ISO utiliza o mesmo raciocínio, primeiro o de maior "tamanho", o ano, depois o mês e por fim o dia. 18 de Março de 1814, por exemplo, seria 1814-03-18. O formato comum no Brasil ― 18/03/1814 ― opera na lógica exatamente inversa. No mundo, os países podem ser divididos em, aproximadamente, [cinco grupos de formato de data](https://en.wikipedia.org/wiki/Date_format_by_country).

### Limitações e Cuidados

Todo mecanismo automático de triagem sofre com possíveis falhas. Seja por deixar passar alguma coisa, seja por marcar como "lixo" algo que não é. Para evitar danos permanentes, o Jarbas não irá excluir os e-mails _de fato_. Ele irá marcar os e-mails com uma label específica e os arquivará, efetivamente tirando eles da caixa de entrada mas sem correr riscos de uma perda real de informações.

## Implementação

Existe uma infinidade de formas que um programa como o Jarbas pode ser implementado. Eu poderia usar de um servidor meu para executar seu código periodicamente, poderia utilizar alguns dos diversos serviços de automação que já existem, etc. No caso,preferi utilizar uma tecnologia que nunca mexi muito ― o [Google Apps Script](https://www.google.com/script/start/).

## Google Apps Script

O Google Apps Script (GAS) é uma linguagem de programação baseada em JavaScript e que possui suporte nativo aos serviços do Google. Se eu tivesse escolhido escrever o Jarbas em Python, por exemplo, e colocado ele para rodar num servidor meu, eu precisaria ter que lidar com toda a parte de autenticação que permitiria que ele interagisse com minha conta de e-mail. Ao utilizar o GAS, toda essa complexidade é gerenciada para mim diretamente pelo Google em si.

Vamos começar a implementação explorando a plataforma. Esse artigo não é um tutorial de GAS e nem _apenas_ um guia sobre a implementação do Jarbas. Eu escrevi esse texto de forma a reproduzir como foi o processo de desenvolvimento ― eu aprendia a linguagem _enquanto_ implementava meu código nela.

Não sou proficiente em GAS e possivelmente minha implementação do Jarbas possui problemas de estilo de código que fariam desenvolvedores mais experientes na plataforma torcer o nariz. No entanto, eu acho esse tipo de desenvolvimento "exploratório" bastante divertido e didático.

### Mandando um e-mail com o GAS

Como vamos mexer com e-mails, acho legal começarmos com uma das coisas mais básicas que podemos fazer com uma conta de e-mail ― mandar uma mensagem. Comece abrindo o painel do GAS [aqui](https://script.google.com/).

Clique em "Novo Script" e você deverá se ver diante de um editor de código que contém as seguintes instruções:

```javascript
function myFunction() {
  
}
```

A referência que usei ao longo do desenvolvimento foi a [documentação oficial](https://developers.google.com/apps-script/reference/). No caso, vamos direto para a [documentação sobre a integração com o GMail](https://developers.google.com/apps-script/reference/gmail/).

Como podemos ver, a classe [`GmailApp`](https://developers.google.com/apps-script/reference/gmail/gmail-app) promete oferecer acesso geral ao GMail, suas mensagens, threads e labels. Ao entrar na documentação e ver a tabela de métodos, um deles me chama a atenção, o [`sendEmail`](https://developers.google.com/apps-script/reference/gmail/gmail-app#sendEmail(String,String,String)).

De fato, a documentação nos conta que esse método pode ser invocado com parâmetros definindo o destinatário, o assunto e o corpo da mensagem. Vamos fazer um teste usando o código de base oferecido pelo GAS quando criamos um novo script.

```javascript
function myFunction() {
    GmailApp.sendEmail("INSIRA SEU EMAIL AQUI", "Olá!", "Como vai você? :D");
}
```

No menu superior do GAS, clique na setinha de "play". Isso irá executar nossa função.

![menu do GAS](/assets/images/jarbas-menu.png)

Ao clicar, você precisará salvar o projeto e dar um nome à - eu usei "teste-jarbas -  ele. Depois de salvar, clique novamente na setinha e um menu aparecerá pedindo por permissões para acessar seu GMail.

Clique no botão "Analisar Permissões". Em seguida aparecerá uma tela para você selecionar sua conta Google, clique nela também. E então você vai ver uma tela meio assustadora:

![permissões do Jarbas](/assets/images/jarbas-permissoes.png)

Bom, essa tela aparece porque seu app não foi submetido para análise. Não há necessidade de se preocupar com isso agora. Clique em "Avançado" e em seguida em "Acessar teste-jarbas (não seguro)". Finalmente aparecerá uma tela para revisar as permissões do aplicativo. Clique em "Permitir"