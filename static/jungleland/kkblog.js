//kkblog ver0.4 js code under jquery 2

//============================================================================
//get the querystring from current page url
function GetUrlParms()    
{
    var args=new Object();   
    var query=location.search.substring(1);//fetch querystring
    var pairs=query.split("&");//split the line with dot   
    for(var   i=0;i<pairs.length;i++)   
    {   
        var pos=pairs[i].indexOf('=');//match for name=value
            if(pos==-1)   continue; 
            var argname=pairs[i].substring(0,pos);//get the name
            var value=pairs[i].substring(pos+1);//get the value
            args[argname]=unescape(value);//store as properties
    }
    return args;
}

//=============================================================================
/*simple modal msgbox
argument:
0str:caption
1str:text
2(optional)function:when hidden,call it.
*/
function showModalMsg()
{
	$("#simple_modal_caption").text(arguments[0]);
	$("#simple_modal_text").text(arguments[1]);
	$("#simple_modal_ok").bind("click",function(){
		$("#simple_modal").modal("hide");
	});
	if(arguments.length==3)
	{
		var callback_func=arguments[2];
		$('#simple_modal').on('hidden',function(){
			callback_func();
			$('#simple_modal').unbind();
		});
	}
	$("#simple_modal").modal("show");
}

//=======================================================
//arguments:
//music_name
function play_bgmusic(music_name)
{
	//using music_list as an array to store music list
	//example:
	//"music name":"url",

	if(music_names.length==0)return;
	var n=0;
	if(music_name==null)
	{
		n=parseInt(music_names.length*Math.random());
		music_name=music_names[n];
	}
	else
		for(var nn=0;nn<music_names.length;nn++)
			if(music_names[nn]==music_name)
			{
				n=nn;
				break;
			}
	$("#audio_bgmusic").attr("src",music_list[music_name]);
	$("#music_list>li").removeClass("active");
	$("#music_list>li.music_list_item_"+n).addClass("active");
	try
	{
		$("#audio_bgmusic")[0].play();
	}
	catch(err)
	{console.log(err);}
}

//=======================================================
//arguments:
//music_list:
function prepare_music_list()
{
	if(music_list.length==0)return;
	var n=0;
	for(s in music_list)
	{
		ss="\'"+s+"\'";
		var item='<li class="music_list_item_'+n+'"><a href="javascript:play_bgmusic('+ss+');">'+s+'</a></li>';
		$(item).insertAfter("#audio_bgmusic");
		n++;
	}
	$("#audio_bgmusic").attr("volume",0.6);
}

//=======================================================
//arguments:
//0(optional):refered comment id
//1(optional):refered article id
function comment_commit()
{
	var cmt_id=arguments[0];
	$.post("/postcomment",{
		"csrfmiddlewaretoken":$("input[name=csrfmiddlewaretoken]").val(),
		"nickname":$("#comment_name").val(),
		"website":$("#comment_website").val(),
		"email":$("#comment_email").val(),
		"message":$("#comment_message").val(),
		"refered_article":arguments[0],
		"refered_comment":arguments[1]
	}).fail(function(){
		showModalMsg("评论失败","评论失败，请确保昵称和留言必填，稍后重试。");
	}).success(function(){
		showModalMsg("评论成功","若新评论未显示，请等待博主审核。",function(){
			fetch_comment_list(cmt_id,1);
			$("#comment_brand").text(comment_brand);
			$("#comment_message").val("");
			refered_comment=null;
			$("#giveup_reply").css("display","none");
		});
	});
}

//=======================================================
//arguments:
function fetch_comment_list(comment_id,pagination)
{
	$("#comment_list").text("正在加载评论列表……");
	$.get("/comment/"+comment_id).success(function(response,status){
		$("#comment_list").hide()
		$("#comment_list").html(response);
		$("#comment_list").fadeIn(1200);
	}).error(function(){
		$("#comment_list").text("评论列表加载失败，请稍后重试。");
	});
}

//=======================================================
function set_bgmusic_auto_play()
{
	$.removeCookie("bgmusic");
	$("#auto-play").css("display","none");
	$("#no-auto-play").fadeIn(300);
}

//=======================================================
function set_bgmusic_not_auto_play()
{
	$.cookie("bgmusic","none",{expires:999});
	$("#no-auto-play").css("display","none");
	$("#auto-play").fadeIn(300);
}

//=======================================================
//type:0weibo 1renren 2twitter 3facebook 4google+
function share_to(type,title)
{
	var info=encodeURIComponent(title+" - "+location.href);

	if(type==0)
		s="http://v.t.sina.com.cn/share/share.php?title="+info;
	else if(type==1)
		s="http://share.renren.com/share/buttonshare.do?link="+encodeURIComponent(location.href)+"&title="+encodeURIComponent(title);
	else if(type==2)
		s="http://twitter.com/home/?status="+info;
	else if(type==3)
		s="http://www.facebook.com/share.php?u="+info;
	else if(type==4)
		s="https://plus.google.com/share?url="+info;
	else if(type==5)
		s="http://shuo.douban.com/!service/share?image=&href="+encodeURIComponent(location.href)+"&name="+encodeURIComponent(title);
	window.open(s);
}

//=======================================================
//get the arguments from url
var args = new Object();
args = GetUrlParms();

$(document).ready(function(){
	$('.back-to-top,.go-up-button').backToTop();
	$('*[data-toggle="tooltip"]').tooltip();
	prepare_music_list();
	if(args["bgmusic"]!="none" && $.cookie("bgmusic")!="none") play_bgmusic(null);
	$("#audio_bgmusic").bind("ended",function(){play_bgmusic(null);});

	if($.cookie("bgmusic")!="none")
		$("#no-auto-play").css("display","block");
	else
		$("#auto-play").css("display","block");
	$("#no-auto-play").click(set_bgmusic_not_auto_play);
	$("#auto-play").click(set_bgmusic_auto_play);

	$("#search_for").click(function(){
		window.href="/search/"+$("#qsearch").val();
		//return false;
	});
});