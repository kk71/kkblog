var kkblogApp=angular.module("kkblogApp",[]);

kkblogApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    //$httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
}]);


kkblogApp.controller("musicBox",["$scope","$http",function($scope,$http){
    // TODO: add music list code
}]);


kkblogApp.controller("comment",["$scope","$http",function($scope,$http){
    $scope.commentType="评论";
    $scope.replyCommentId=0;

    $http.get('/comment-list/?articleId='+articleId).success(function(data, status, headers, config) {
        $scope.commentList=data["comments"];
    }).error(function(data, status, headers, config) {
        $scope.errorFlag=true;
    });

    $scope.postComment=function(comment){
        $http.post('/post-comment/', {
            nickname:comment.nickname,
            email:comment.email,
            website:comment.website,
            message:comment.message,
            articleId:articleId,
            replyCommentId:String($scope.replyCommentId)
        }).success(function(data, status, headers, config) {
            if(commentVerify)
                sweetAlert("成功","留言成功，需要等博主审核才能显示。","success");
            else
                sweetAlert("成功","留言成功。","success");
        }).error(function(data, status, headers, config) {
            sweetAlert("失败","请检查网络，稍后重试。","error");
        });
    };

    $scope.reply=function(id,nickname){
        $scope.replyCommentId=id;
        $scope.commentType="回复 "+nickname;
    };

    $scope.noReply=function(){
        $scope.replyCommentId=0;
        $scope.commentType="评论";
    };
}]);


kkblogApp.controller("shareBox",["$scope","$http",function($scope,$http){

    //type:0weibo 1renren 2twitter 3facebook 4google+
    $scope.shareTo=function(type,title){
        var info=encodeURIComponent(title+" - "+location.href);

        if(type==0)
            s="http://v.t.sina.com.cn/share/share.php?title="+info;
        else if(type==1)
            s="http://share.renren.com/share/buttonshare.do?link="+encodeURIComponent(location.href)+"&title="+encodeURIComponent(title);
        else if(type==2)
            s="http://shuo.douban.com/!service/share?image=&href="+encodeURIComponent(location.href)+"&name="+encodeURIComponent(title);
        else if(type==3)
            s="http://twitter.com/home/?status="+info;
        else if(type==4)
            s="http://www.facebook.com/share.php?u="+info;
        else if(type==5)
            s="https://plus.google.com/share?url="+info;
        window.open(s);
    }
}]);


$(document).ready(function(){
	$('.back-to-top,.go-up-button').backToTop();
});