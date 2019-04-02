/**
 * Created by xjk on 2018/3/26.
 */
var startTime = currentTime(); // 启动时间
var startPercent = 0;
var isStarted = false; // 是否启动

while(true) {
    setTimeOut(function(){isStarted = true },5000);
    if(!isStarted) {
         var time = currentTime() - startTime;
         startPercent = time / (time + 10)
         console.log(startPercent)
    }else{
         startPercent = 1 // 哗啦跳到100%
         break;
    }
}
