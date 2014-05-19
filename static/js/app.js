var app = {
	offer:null,
	init:function(){
			
		$(document).ajaxStop($.unblockUI);
		$('form').on('submit', app.search);
		$('#comprar').on('click', app.comprar);
		
		$('#one').grumble({
			text:"Para iniciar o nosso tour, adicione a url da oferta HU que você deseja pesquisar.",
			angle:200,
			distance:3,
			hideOnClick:true
		});
		
		$('#one').on('input', function(){
			$('#one').grumble('hide');
		});
		
		app.load();
	},
	comprar:function(){
		window.open(app.offer.link.concat("#botao-comprar-oferta"));
	},
	createMarker:function(params){
		var image = {
			/**
			 * Icone default do HU.
			 */
			size:new google.maps.Size(20, 32),
			origin:new google.maps.Point(0,0),
			anchor: new google.maps.Point(0,32)
		}

		var shape = {
			coord:[10, 1, 1, 20, 18, 20, 18 , 1],
			type:'poly'
		}
		return new google.maps.Marker(params)
	},
	detailOffer:function(){
		/**
		 * Define informações de tooltip.
		 */
			try{ $('#title-oferta').tooltipster('destroy') }catch(e){ /**/ }
			$('#title-oferta').tooltipster({
				theme: 'tooltipster-shadow',
				content:$("<img src='"+app.offer.src+"'/>")
			});
		
		/**
		 * Titulo da oferta.
		 */
			$('#title-oferta').html(app.offer.title);
			$('#information-about-player').fadeIn();
		
		/**
		 * Marca ofeta no mapa.
		 */
			var hotelLatLng = new google.maps.LatLng(app.offer.lat, app.offer.lng);
			var marker = app.createMarker({
							position:hotelLatLng,
							icon: window.location.href.concat('static/img/logo-hu.png'),
							map:app.map,
							draggable:false,
							animation: google.maps.Animation.DROP,
							id:app.offer.id
			});
			
			app.map.setZoom(15);
			app.map.panTo(marker.position);
			
			$('#title-oferta').grumble({
				text:"Passe o mouse sobre a titulo da oferta para você visualizar a foto principal.",
				angle:200,
				distance:3,
				hideOnClick:true
			});
			
			$('#title-oferta').on('mouseover', function(){
				$('#title-oferta').grumble('hide');
			});
	},
	load:function(){
		var mapOptions = {
			zoom:10,
			/**
			 * Foco principal do mapa:
			 */
			mapTypeId: google.maps.MapTypeId.ROADMAP,
			scaleControl:false,
			streetViewControl:false,
			mapTypeControl:false
		}

		/**
		 * Iniciar map, com geo de inicialização.
		 */
		 app.map = new google.maps.Map($('#map-canvas')[0], mapOptions);
		 if( navigator.geolocation ){
			navigator.geolocation.getCurrentPosition(app.geo);
		 }
	},
	search:function(){		
		$.blockUI({ message: '<img src="/static/img/logo-hu-carregando.gif" />'});
		$.getJSON('/offer.json', {q:$("input[name=q]", this).val()})
			.done(function(response){
				/***
				 * Recarrega ponto central no map.
				 */
					app.offer = response.offer;
					app.map.setCenter(new google.maps.LatLng(response.offer.lat, response.offer.lng));
					
				$.each(response.photos, function(j, n){
					/***
				 	 * Marcar photos no mapa.
				 	 */
						var hotelLatLng = new google.maps.LatLng(n.lat, n.lng);
						var marker = app.createMarker({
										position:hotelLatLng,
										icon: window.location.href.concat('static/img/Active-Instagram-3-icon.png'),
										map:app.map,
										title:n.title,
										src:n.src,
										zIndex:1,
										id:j,
										link:n.link,
										distance:n.distance,
										draggable:false
						});
						
						var info = new google.maps.InfoWindow();
						google.maps.event.addListener(marker, 'click', function(){
							app.goToDetail({self:this});
						});

						google.maps.event.addListener(marker, 'mouseover', function(){
							var source = $('#tooltips-google-template').html(),
								template = Handlebars.compile(source),
								html = template({src:this.src, distance:this.distance});
								
							info.setContent(html);
							info.open(app.map, this);
						});

						google.maps.event.addListener(marker, 'mouseout', function(){
							info.close(app.map, this);
						})
				});
				
				app.detailOffer();
			});
		return false;
	},
	geo:function(position){
		app.map.setCenter(new google.maps.LatLng(position.coords.latitude, position.coords.longitude));
	},
	goToDetail:function(options){
		window.open(options.self.link);
	}
}
google.maps.event.addDomListener(window, 'load', app.init);