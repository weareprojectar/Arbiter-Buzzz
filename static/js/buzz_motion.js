( function($) {
    
    $(window).load(function(){
        var cont_svg1 = $('#buzz_indent_motion1>svg');
        var cont_svg1_count = cont_svg1.children('.inde_line1').length;
        
        var path1 = MorphSVGPlugin.pathDataToBezier("#buzz_indent_motion1>svg>#line1");
        
        for(var i=0; i<cont_svg1_count; i++){
            TweenMax.to('#buzz_indent_motion1>svg>#indent1_motion'+(i+1)+'', 10, {
                bezier:{values:path1, type:"cubic"},
                ease:Power0.easeNone,
                repeat:-1,
                delay:0.2*i
            });
        }
        
        var cont_svg2 = $('#buzz_indent_motion2>svg');
        var cont_svg2_count = cont_svg2.children('.inde_line2').length;
        
        var path2 = MorphSVGPlugin.pathDataToBezier("#buzz_indent_motion2>svg>#line2");
        
        setTimeout(function(){
            for(var j=0; j<cont_svg2_count; j++){
                TweenMax.to('#buzz_indent_motion2>svg>#indent2_motion'+(j+1)+'', 10, {
                    bezier:{values:path2, type:"cubic"},
                    ease:Power0.easeNone,
                    repeat:-1,
                    delay:0.2*j
                });
            }    
        }, 1000);
        
        
        var cont_svg3 = $('#buzz_indent_motion3>svg');
        var cont_svg3_count = cont_svg3.children('.inde_line3').length;

        var path3 = MorphSVGPlugin.pathDataToBezier("#buzz_indent_motion3>svg>#line3");

        setTimeout(function(){
            for(var k=0; k<cont_svg3_count; k++){
                TweenMax.to('#buzz_indent_motion3>svg>#indent3_motion'+(k+1)+'', 10, {
                    bezier:{values:path3, type:"cubic"},
                    ease:Power0.easeNone,
                    repeat:-1,
                    delay:0.2*k
                });
            }
        }, 3000);
        
        
        var cont_svg4 = $('#buzz_indent_motion4>svg');
        var cont_svg4_count = cont_svg4.children('.inde_line4').length;

        var path4 = MorphSVGPlugin.pathDataToBezier("#buzz_indent_motion4>svg>#line4");
        
        setTimeout(function(){
            for(var l=0; l<cont_svg4_count; l++){
                TweenMax.to('#buzz_indent_motion4>svg>#indent4_motion'+(l+1)+'', 10, {
                    bezier:{values:path4, type:"cubic"},
                    ease:Power0.easeNone,
                    repeat:-1,
                    delay:0.2*l
                });
            }
        }, 2000);
        
        
    });
   
    
})(jQuery);