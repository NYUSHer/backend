(function() {

    // let BASEURI = "https://nyu.nekoyu.cc:6680";  // server mode
    let BASEURI = "http://localhost:8080"; // localtest mode
    let $refreshButton = $("#search");
    let $buttonClick = $("#searchSub");
    let $D2A1 = $("#D2A1");
    let $D2A2 = $("#D2A2");
    let $A2D1 = $("#A2D1");
    let $A2D2 = $("#A2D2");
    var clicked = false;

    // $buttonClick.on("submit", e => {
    //     e.preventDefault();
    //     refresh();
    // });

    // auto load bus schedule
    $( document ).ready(function() {
        refresh();
    });
    
    $( "#widget" ).click(function() {
        if (clicked == false) {
            window.location.hash = "2";
            clicked = true;
        } else {
            window.location.hash = "1";
            clicked = false;
        }
      });
    
    function submission() {
        $searchButton.addClass("loading");
        refresh();
    }

    function refresh() {
        let uri = `${BASEURI}/widgets/bus`;

        axios.get(uri)
             .then(function(response) {
                let data = response.data;
                $refreshButton.removeClass("loading");
                refreshTime(data);
             })
             .then(function(error) {});
    }

    function refreshTime(timetable) {
        let html1 = `${timetable['dorm2campus'][0][0]},  ${timetable['dorm2campus'][0][1]} bus(es)`;
        $D2A1.html(html1);
        let html2 = `${timetable['dorm2campus'][1][0]},  ${timetable['dorm2campus'][1][1]} bus(es)`;
        $D2A2.html(html2);
        let html3 = `${timetable['campus2dorm'][0][0]},  ${timetable['campus2dorm'][0][1]} bus(es)`;
        $A2D1.html(html3);
        let html4 = `${timetable['campus2dorm'][1][0]},  ${timetable['campus2dorm'][1][1]} bus(es)`;
        $A2D2.html(html4);
    }
})();
