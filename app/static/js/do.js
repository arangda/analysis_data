$(document).ready(function(){
    $("#clear").click(function(){
        is_clear = confirm("你确认要删除所有表吗？");
        $.getJSON("/index",{
            clear:"clear"
        },function(data){
            console.log(data)
            location.href="/index"

        })
    })
})