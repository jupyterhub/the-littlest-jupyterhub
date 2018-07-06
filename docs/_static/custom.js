// Set up copy/paste for code blocks
function addCopyButtonToCode(){
  // get all <code> elements
  var allCodeBlocksElements = $( "div.highlight pre" );

  allCodeBlocksElements.each(function(ii) {
   	// add different id for each code block

  	// target
    var currentId = "codeblock" + (ii + 1);
    $(this).attr('id', currentId);

    //trigger
    var clipButton = '<button class="btn copybtn" data-clipboard-target="#' + currentId + '"><img src="https://clipboardjs.com/assets/images/clippy.svg" width="13" alt="Copy to clipboard"></button>';
       $(this).after(clipButton);
    });

    new Clipboard('.btn');
}

$(document).ready(function () {
  // Highlight current page in sidebar
  console.log('hi');
  addCopyButtonToCode();
});
