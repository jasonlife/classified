<!DOCTYPE html>
<html>

   <head>
      <meta charset = "utf-8" />
      <link href = 'http://fonts.googleapis.com/css?family=Play:400,700' 
         rel = 'stylesheet' type = 'text/css'>
      <link rel = "stylesheet" href = "assets/css/style.css">
      <link rel = "stylesheet" href = "src/blockrain.css">
   </head>
	
   <body>
	
      <section id = "examples">
		
         <article id = "example-slider">
			
            <div class = "example">
				
               <div class = "instructions">
					
                  Use only arrows
						
                  <div class = "keyboard">
                     <div class = "key key-up"></div>
                     <div class = "key key-left"></div>
                     <div class = "key key-down"></div>
                     <div class = "key key-right"></div>
                  </div>
						
               </div>
					
               <div class = "game" id = "tetris-demo"></div>
            </div>
				
         </article>
			
      </section>
		
      <script src = "assets/js/jquery-1.11.1.min.js"></script>
      <script src = "src/blockrain.jquery.libs.js"></script>
      <script src = "src/blockrain.jquery.src.js"></script>
      <script src = "src/blockrain.jquery.themes.js"></script>

      <script>
         var $cover = $('#cover-tetris').blockrain({
            autoplay: true,
            autoplayRestart: true,
            speed: 100,
            autoBlockWidth: true,
            autoBlockSize: 25,
            theme: 'candy'
         });

         var versusSpeed = 500;
			
         var $versus1 = $('#tetris-versus-1 .game').blockrain({
            autoplay: true,
            autoplayRestart: true,
            speed: versusSpeed,
				
            onGameOver: function() {
               $versus1.blockrain('restart');
               $versus2.blockrain('restart');
               var $score = $versus2.parent().find('.score');
               $score.text( parseInt($score.text()) + 1 );
            }
				
         });
			
         var $versus2 = $('#tetris-versus-2 .game').blockrain({
            autoplay: true,
            autoplayRestart: true,
            speed: versusSpeed,
				
            onGameOver: function() {
               $versus1.blockrain('restart');
               $versus2.blockrain('restart');
               var $score = $versus1.parent().find('.score');
               $score.text( parseInt($score.text()) + 1 );
            }
				
         });

         var $demo = $('#tetris-demo').blockrain({
            speed: 20,
            theme: 'black',
				
            onStart: function() {
               ga( 'send', 'event', 'tetris', 'started');
            },
				
            onLine: function() {
               ga( 'send', 'event', 'tetris', 'line');
            },
				
            onGameOver: function(score){
               ga( 'send', 'event', 'tetris', 'over', score);
            }
				
         });

         $('#example-slider').find('.btn-next').click(function(event){
            event.preventDefault();
            switchDemoTheme(true);
         });
			
         $('#example-slider').find('.btn-prev').click(function(event){
            event.preventDefault();
            switchDemoTheme(false);
         });

         function switchDemoTheme(next) {

            var themes = Object.keys(BlockrainThemes);

            var currentTheme = $demo.blockrain('theme');
            var currentIx = themes.indexOf(currentTheme);

            if( next ) { currentIx++; }
            else { currentIx--; }

            if( currentIx > = themes.length ){ currentIx = 0; }
            if( currentIx < 0 ){ currentIx = themes.length-1; }

            $demo.blockrain('theme', themes[currentIx]);
            $('#example-slider .theme strong').text( '"'+themes[currentIx]+'"' );
         }
			
      </script>
		
   </body>

</html>
