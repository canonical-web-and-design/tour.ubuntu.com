/*
* Software Centre System
*  author: Anthony Dillon
*/

function SoftwareSystem($parent){
	var _this = this;
	var _parent = $parent;
	var minified = false;
	var maximised = false;
	var _isOpen = false;
	var currentApp = null;
	var installedApps = new Array();
	var thePrice = '';
	var theName = '';
	var theSub = '';
	var theImage = '';
	var theDescription = '';
	var theDesctiptionImage = '';
	
	this.init = function(){
		
		$('#software-centre .loading-bar').hide();
		$('#software-centre .detailed .price .progress').css('width','0');
		
		$('#software-centre .control .close').click(function(){
			_this.close();
		});
		$('#software-centre  .control .min').click(function(){
			_this.min();
		});
		
		$('#software-centre  .control .max').click(function(){
			if(maximised){
				maximised = false;
				$('#software-centre').removeClass('fullsize');
				_parent.systemSettings.decreaseFullscreen();
			}else{
				maximised = true;
				$('#software-centre').addClass('fullsize');
				_parent.systemSettings.increaseFullscreen();
			}
			_this.resize();
		});
		
		$('#software-centre .top-panel .back').bind('click',function(){
			if(!$(this).hasClass('disabled')){
				$('#software-centre .home').show();
				$('#software-centre .detailed').hide();
				$(this).addClass('disabled');
				$('#software-centre .top-panel .forward').removeClass('disabled');
			}
		});
		$('#software-centre .top-panel .forward').bind('click',function(){
			if(!$(this).hasClass('disabled')){
				_this.loadApp();
				$(this).addClass('disabled');
			}
		});
		
		$('#software-centre .whats-new .app-container div').click(function(){
			currentApp = $(this).attr('class');
			$('#software-centre .top-panel .forward').addClass('disabled');
			_this.loadApp();
		});
		this.setupInstall();
		this.setupTopButtons();
		this.center();
	}
	
	this.loadApp = function(){
		var error = false;
		$('#software-centre .top-panel .back').removeClass('disabled');
		$('#software-centre .detailed .price .theprice').removeClass('installed');
		$('#software-centre .detailed .price .button').text('Install');
		if(installedApps[currentApp] == true){  _this.installedApp(); }
		switch(currentApp){
				case 'chromium':
					thePrice = 'Free';
					theName = 'Chromium Web Browser';
					theSub = 'Access the Internet';
					theImage = 'img/software-centre/logo-chromium.png';
					theDescription = 'Chromium is an open-source browser project that aims to build a safer, faster, and more stable way for all Internet users to experience the web.<br/><br/>Chromium serves as a base for Google Chrome, which is Chromium rebranded (name and logo) with very few additions such as usage tracking and an auto-updater system.<br/><br/>This package contains the Chromium browser';
					theDesctiptionImage = 'img/software-centre/screenshot-chromium.jpg';
				break;
				case 'beep':
					thePrice = '$9.99';
					theName = 'BEEP';
					theSub = 'A 2D platformer/shooter game with physics-based puzzels';
					theImage = 'img/software-centre/logo-beep.png';
					theDescription = 'BEEP is a 2D side-scrolling platformer with physics-based gameplay. You control a small robot equipped with an anti-gravity device, a jet-pack and a gun. Drive, jump, fly, swim and shoot your way through 24 levels scattered across 6 unique environments.<br/><br/>Use BEEP’s anti-gravity device to directly manipulate the physics-based environments. The anti-gravity device is both a tool and a weapon. Use it to smash enemy robots, build towers and solve puzzles.<br/><br/>BEEP has traveled for thousands of years through deep space to explore the Galaxy. Traverse a foreign star system with the BEEP-ship and send robots to the surface of the planets.';
					theDesctiptionImage = 'img/software-centre/screenshot-beep.jpg';
				break;
				case 'inkscape':
					thePrice = 'Free';
					theName = 'Inkscape Vector Graphics Editor';
					theSub = 'Create and edit Scalable Vector Graphics images';
					theImage = 'img/software-centre/logo-inkscape.png';
					theDescription = 'Inkscape loads and saves a subset of the SVG (Scalable Vector Graphics) format, a standard maintained by the WWW consortium.<br/><br/>Inkscape user interface should be familiar from CorelDraw and similar drawing programs. There are rectangles, ellipses, text items, bitmap images and freehand curves. As an added bonus, both vector and bitmap objects can have alpha transparency and can be arbitrarily transformed.<br/><br/>Inkscape supports multiple opened files and multiple views per file. Graphics can be printed and exported to png bitmaps.<br/><br/>Some of the import and export features are provided using the packages dia, libwmf-bin, pstoedit, skencil, imagemagick, and perlmagick.<br/><br/>Other extensions use ruby, libxml-xql-perl, python-numpy, and python-lxml. You must have these packages to make full use of all extensions and effects.<br/><br/>If you want to use the spellchecker, you have to install aspell and the respective language-pack, e.g. aspell-en or aspell-de.';
					theDesctiptionImage = 'img/software-centre/screenshot-inkscape.jpg';
				break;
				case 'worldofgoo':
					thePrice = '$19.95';
					theName = 'World of Goo';
					theSub = 'Physics based pzzle/construction game';
					theImage = 'img/software-centre/logo-world-of-goo.png';
					theDescription = 'Drag and drop living, squirming, talking globs of goo to build structures, bridges, cannonballs, zeppelins, and giant tongues. The millions of innocent goo balls that live in the beautiful World of Goo are curious to explore.<br/><br/>But they dont know that they are in a game, or that they are extremely delicious. The most addicting and awe-inspiring puzzle game will set you on an adventure that youll never forget!';
					theDesctiptionImage = 'img/software-centre/screenshot-worldofgoo.jpg';
				break;
				case 'blender':
					thePrice = 'Free';
					theName = 'Blender';
					theSub = 'Create and edit 3D models and animations';
					theImage = 'img/software-centre/logo-blender.png';
					theDescription = 'Blender is an integrated 3d suite for modelling, animation, rendering, post-production, interactive creation and playback (games). Blender has its own particular user interface, which is implemented entirely in OpenGL and designed with speed in mind. Python bindings are available for scripting; import/export features for popular file formats like 3D Studio and Wavefront Obj are implemented as scripts by the community. Stills, animations, models for games or other third party engines and interactive content in the form of a standalone binary and/or a web plug-in are common products of Blender use.';
					theDesctiptionImage = 'img/software-centre/screenshot-blender.jpg';
				break;
				case 'braid':
					thePrice = '$9.99';
					theName = 'Braid';
					theSub = 'Manipulate the flow of time to solve puzzels';
					theImage = 'img/software-centre/logo-braid.png';
					theDescription = 'Manipulate the flow of time to solve puzzles Braid is a platform game in painterly style where you manipulate the flow of time to solve puzzles. Every puzzle in Braid is unique;  there is no filler.<br/><br/>Braid treats your time and attention as precious, and it does everything it can to give you a mind-expanding experience.<br/><br/>All gameplay is based on time manipulation. Journey into worlds where time behaves strangely; observe, learn from, and then master these worlds.';
					theDesctiptionImage = 'img/software-centre/screenshot-braid.jpg';
				break;
				default:
					_parent.errorMessage.open();
					error = true;
					break;	
				}
			
			$('#software-centre .detailed .title h1').text(theName);
			$('#software-centre .detailed .title p.subheading').text(theSub);
			$('#software-centre .detailed .title img.app-image').attr('src', theImage);
			$('#software-centre .detailed .description').html(theDescription);
			$('#software-centre .detailed .description-image img').attr('src',theDesctiptionImage);
			if($('#software-centre .detailed .price .theprice').hasClass('installed')){
				$('#software-centre .detailed .price .theprice').text('Installed');
			}else{
				$('#software-centre .detailed .price .theprice').text(thePrice);
			}
			if(!error){
				$('#software-centre .home').hide();
				$('#software-centre .detailed').show();
			}
	}
	
	this.setupInstall = function(){
		$('#software-centre .detailed .price .button').bind('click',function(){
			if(installedApps[currentApp] == true){
				_this.removeApp();
			}else{
				$(this).hide();
				$('#software-centre .loading-bar').show();
				$('#software-centre .detailed .price .theprice').text('Installing…');
				$('#software-centre .loading-bar .progress').animate({
				    	width: 150
				  }, 1500, function() {
				    	_this.installedApp();
						$('#software-centre .loading-bar').hide();
						$('#software-centre .detailed .price .button').show();
				  });
				 }
		});
	}
	
	this.removeApp = function(){
		$('#software-centre .detailed .price .theprice').text(thePrice);
		$('#software-centre .detailed .price .theprice').removeClass('installed');
		$('#software-centre .detailed .price .theprice').css('background-image','none');
		$('#software-centre .detailed .price .button').text('Install');
		_parent.systemOverlay.removeApps(theName);
		installedApps[currentApp] = false;
	}
	
	this.installedApp = function(){
		$('#software-centre .detailed .price .theprice').text('Installed');
		$('#software-centre .detailed .price .theprice').addClass('installed');
		$('#software-centre .detailed .price .button').text('Remove');
		$('#software-centre .detailed .price .progress').css('width','0');
		_parent.systemOverlay.totalApps.push({name:theName,image:theImage});
		installedApps[currentApp] = true;
	}
	
	this.setupTopButtons = function(){
		$('#software-centre .all-software').bind('click', function(){
			$('#software-centre .home').show();
			$('#software-centre .detailed').hide();
			$('#software-centre .top-panel .back').addClass('disabled');
		});
	}
	
	this.close = function(){
		if(_isOpen){
			$('#software-centre .home').show();
			$('#software-centre .detailed').hide();
			if(maximised){ _parent.systemSettings.decreaseFullscreen(); }
			$('#software-centre ').hide();
			_parent.systemMenu.closeWindow('software');
			$('#software-centre ').removeClass('fullsize');
			_this.resize();
			minified = _isOpen = false;
			_this.center();
			if($('css3-container').length > 0){
	        	$('#software-centre').prev().css('top', $('#software-centre').css('top'));
	        	$('#software-centre').prev().css('left', $('#software-centre').css('left'));
	        }
       }
	}
	
	this.min = function(){
		if(maximised){ _parent.systemSettings.decreaseFullscreen(); }
		$('#software-centre ').hide();
		_parent.systemMenu.wiggle('software');
		minified = true;
	}
	
	this.resize = function(){
		var containerHeight = $('#software-centre').height() - ($('#software-centre .top-panel').height() + $('#software-centre .control').height() + 6);
		var appBoxWidth = $('#software-centre').width() - ($('#software-centre .navigation').width() + 50);
    	if(maximised){ containerHeight -= 27; }
		$('#software-centre .container').css('height',containerHeight);
		$('#software-centre .container .whats-new').css('width',appBoxWidth);
	}
	
	this.center = function(){
    	var left = ($(document).width() / 2) - ($('#software-centre ').width() / 2);
		var top = Math.max(24,($(document).height() / 2) - ($('#software-centre ').height() / 2));
		$('#software-centre ').css('left',left);
		$('#software-centre ').css('top',top);
    }
    
    this.isMaximised = function(){
		return maximised;
	}
	
	this.open = function($app){
		if($app != undefined){ currentApp = $app; this.loadApp(); }
		this.resize();
		this.center();
		$('#software-centre').show();
		_isOpen = true;
		_parent.systemMenu.openWindow('software');
		if($('css3-container').length > 0){
        	$('#software-centre').prev().css('top', $('#software-centre').css('top'));
        	$('#software-centre').prev().css('left', $('#software-centre').css('left'));
        }
	}
}