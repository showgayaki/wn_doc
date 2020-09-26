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
        $('#code-wrap').empty();
        $('#code-wrap').append(codeTitleTag + thisId + '</h4>');
        $('#code-wrap').append(codeArea);

        getWritten(codes[thisId]['code'], function(html){
            if(thisId === 'README.md'){
                html = marked(shapeHtml(html));
                $('#code-area').addClass('markdown px-3 border');
                $('#code-area').append(html);
            }else if(thisId.split('.').reverse()[0] === 'ipynb'){
                $('#code-area').append(html);
                const gistData = $('.gist-data').html();
                ipynb2Html(gistData, '#code-area');
                $(document).ready(function() {
                    $('pre code').each(function(i, block) {
                        hljs.highlightBlock(block);
                    });
                });
            }else{
                $('#code-area').append(html);
            }
        });
    });
});

function shapeHtml(html){
    // いらないタグ削除
    shapedHtml = html.replace(/<br>/g, '\n').replace(/<("[^"]*"|'[^']*'|[^'">])*>/g, '');
    // おしりに残ったprettyPrint();と、前後の空白削除
    shapedHtml = shapedHtml.replace('prettyPrint();', '').trim();
    // コードエリアの空白コードを半角スペースに変更、空白コードを改行に変更
    shapedHtml = shapedHtml.replace(/&nbsp; /g, ' ').replace(/&nbsp;/g, '<br>');
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