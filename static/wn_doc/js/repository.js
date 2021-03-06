$(function(){
    const codeTitleTag = '<h4 class="file-name p-2 mb-0 text-light">';
    const codeArea = '<div id="code-area" class="code-area"></div>';

    if(codes['README.md']){
        // コンテンツ部分を取得
        const html = $('.prettyprint').html();
        // いったん空にしてから整形したコンテンツを追加
        $('#code-wrap').empty();
        $('#code-wrap').append(codeTitleTag + 'README.md</h4>');
        $('#code-wrap').append(codeArea);

        const markUp = marked(shapeHtml(html, true));
        $('#code-area').append(markUp);
        $('#code-area').addClass('markdown px-3 border');
    }

    // ファイルクリック時
    $('a.blob').on('click', function(){
        const thisId = $(this).attr('id');
        const fileExtension = thisId.split('.').reverse()[0]
        $('#code-wrap').empty();
        $('#code-wrap').append(codeTitleTag + thisId + '</h4>');
        $('#code-wrap').append(codeArea);

        getWritten(codes[thisId]['code'], function(html){
            if(thisId === 'README.md'){
                html = marked(shapeHtml(html, true));
                $('#code-area').append(html);
                $('#code-area').addClass('markdown px-3 border');
                return;
            }
            else{
                const langType = languageType(fileExtension);
                if(langType === 'ipynb'){
                    $('#code-area').append(html);
                    const gistData = $('.gist-data').html();
                    ipynb2Html(gistData, '#code-area');
                }else{
                    const codeRows = shapeHtml(html, false).split('\n');
                    let rows = '';
                    for(let i = 0; i < codeRows.length; i++){
                        rows += '<span class=\"row-num\">' + String(i + 1) + '</span>' + codeRows[i] + '\n';
                    }
                    html = '<pre><code class=\"' + langType + '\">' + rows + '</code></pre>'
                    $('#code-area').append(html);
                }
                $(document).ready(function(){
                    $('pre code').each(function(i, block){
                        hljs.highlightBlock(block);
                    });
                });

                $('#code-area').addClass('m-0 border');
                $('#code-area pre').addClass('p-0 py-2 pr-3 mb-0');
            }
        });
    });
});

function shapeHtml(html, isReadme){
    // いらないタグ削除
    shapedHtml = html.replace(/<br>/g, '\n').replace(/<("[^"]*"|'[^']*'|[^'">])*>/g, '');
    // おしりに残ったprettyPrint();と、前後の空白削除
    shapedHtml = shapedHtml.replace(/\nprettyPrint\(\);/g, '').trim();
    if(isReadme){
        // コードエリアの空白コードを半角スペースに変更、空白コードを改行に変更
        shapedHtml = shapedHtml.replace(/&nbsp; /g, '  ').replace(/&nbsp;/g, '<br>');
        // ```HTML```用
        shapedHtml = shapedHtml.replace(/&lt;/g, '<').replace(/&gt;/g, '>');
    }
    return shapedHtml;
}


function getWritten(fileName, callback) {
    const $iframe = $('<iframe hidden\/>');
    // iframe が DOM 上に存在しないとうまくいかないので一時的に出力する
    $iframe.appendTo('#code-wrap');
    const frameDocument = $iframe[0].contentWindow.document;
    const scriptTag = '<script src=\"' + fileName + '\"><\/script>';
    frameDocument.open();
    // frame 内での window.setResult に結果受信用関数を作成する
    $iframe[0].contentWindow.setResult = function(html) {
        // 親フレーム上から用済みの iframe を除去する
        $iframe.remove();
        // 取得した文字列には scriptTag が含まれているので削除してコールバックに渡す
        callback(html.replace(scriptTag, ''));
    };
    frameDocument.write(
        '<div id=\"area-to-write\">' +
        // div タグ内に scriptTag を貼る
        scriptTag +
        '<\/div>' +
        '<script>' +
        // div タグ内に出力された文字列を setResult() に渡す
        'setResult(document.querySelector(\"#area-to-write\").innerHTML);' +
        '<\/script>'
    );
    frameDocument.close();
}


function languageType(extension){
    // サポート言語一覧
    // https://github.com/highlightjs/highlight.js/blob/master/SUPPORTED_LANGUAGES.md
    let langType = '';
    switch(extension){
        case 'py':
            langType = 'python';
            break;
        case 'ipynb':
            langType = 'ipynb';
            break;
        case 'xml':
            langType = 'xml';
            break;
        case 'html':
            langType = 'html';
            break;
        case 'js':
            langType = 'javascript';
            break;
        case 'ejs':
            langType = 'html';
            break;
        case 'css':
            langType = 'css';
            break;
        case 'sh':
            langType = 'bash';
            break;
        case 'bat':
            langType = 'bat';
            break;
        case 'json':
            langType = 'json';
            break;
        case 'cs':
            langType = 'csharp';
            break;
        case 'ps1':
            langType = 'powershell';
            break;
        case 'scss':
            langType = 'scss';
            break;
        case 'coffee':
            langType = 'coffeescript';
            break;
        case 'rb':
            langType = 'ruby';
            break;
        case 'yaml':
            langType = 'yaml';
            break;
        case 'rb':
            langType = 'ruby';
            break;
        case 'php':
            langType = 'php';
            break;
        case 'ini':
            langType = 'ini';
            break;
        case 'ts':
            langType = 'typescript';
            break;
        default:
            langType = 'plaintext';
            break;
      }
      return langType;
}
