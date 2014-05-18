var app = {
	offer:null,
	init:function(){		
		$(document).ajaxStop($.unblockUI);
		$('form').on('submit', app.search);
		$('#comprar').on('click', app.comprar);
		app.load();
	},
	comprar:function(){
		window.open(app.offer.link);
	},
	detailOffer:function(){
		try{ $('#title-oferta').tooltipster('destroy') }catch(e){ /**/ }
		$('#title-oferta').tooltipster({
			theme: 'tooltipster-shadow',
			content:$("<img src='"+app.offer.src+"'/>")
		});
		
		$('#title-oferta').html(app.offer.title);
		$('#information-about-player').fadeIn();
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
						var image = {
							/**
							 * Icone default do HU.
							 */
							//url: 'images/beachflag.png',
							size:new google.maps.Size(20, 32),
							origin:new google.maps.Point(0,0),
							anchor: new google.maps.Point(0,32)
						}

						var shape = {
							coord:[10, 1, 1, 20, 18, 20, 18 , 1],
							type:'poly'
						}

						var hotelLatLng = new google.maps.LatLng(n.lat, n.lng);
						var marker = new google.maps.Marker({
										position:hotelLatLng,
										map:app.map,
										shape:shape,
										title:n.title,
										src:n.src,
										zIndex:1,
										id:j,
										link:n.link,
										distance:n.distance
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