(function() {

    $('.ui.accordion').accordion();
    $('.ui.dropdown').dropdown();
    Bmob.initialize("1fe041375281fb38612829308c8b2f06", "5e2d348f45b02e6915c8be18e384e335");
    
    let BASEURI = "http://api-sp.nyu.wiki"; // server mode
    // let BASEURI = "http://localhost:8080"; // localtest mode
    let $search = $("#search");
    let $text = $("#searchText");
    let $searchSub = $("#searchSub");
    let $courseListBar = $("#courseListBar");

    $searchSub.on("submit", e => {
        let option = $("#selectOption").val();
        e.preventDefault();
        submission(option);
    });

    function generateColorByName(name) {
        let hash = forge.md.md5.create();
        hash.update(name);
        let hashstr = hash.digest().toHex();
    
        return `rgb(${parseInt("0x" + hashstr.substr(0,2))},${parseInt("0x" + hashstr.substr(2,2))},${parseInt("0x" + hashstr.substr(4,2))})`;
    }
    
    function whiteRate(c) {
        let begin = c.search(/\(/);
        let end = c.search(/\)/);
        let colors = c.substring(begin + 1, end).split(",");
        let v = 0;
        for (var i = 0; i < colors.length; i++) {
            v += parseInt(colors[i]) / 255 / colors.length;
        }
        return v > 0.5 ? "#000" : "#FFF";
    }

    function submission(option=null) {
        let text = $text.val().trim();
        if (!text) return;

        $search.addClass("loading");
        searchItem(text, option);
    }

    function searchItem(text, option) {
        let myOption = option;
        let uri = `${BASEURI}/course?keyword=${text}`;
        if (option == "faculty") uri = `${BASEURI}/faculty?keyword=${text}`;

        axios.get(uri)
             .then(function(response) {
                let data = response.data;
                $search.removeClass("loading");
                if (option == "faculty") {
                    refreshList([{
                        course_id: "-1",
                        course_title: "Searched Professor",
                        term_descr: "keyword",
                        class_type_descr: $text.val().trim()
                    }]);
                    setTimeout(function() { $('.ui.accordion').accordion("open", 0); }, 100);
                    generateExtending("-1", response.data);
                } else {refreshList(data);}
             })
             .then(function(error) {});
    }

    function getFaculties(cid) {
        let myCid = cid;
        axios.get(`${BASEURI}/class?course_id=${cid}`)
             .then(function(response) {
                generateExtending(myCid, response.data);
             })
             .then(function(error) {});
    }

    function getRate(nid, callback){
        var Data = Bmob.Object.extend("AllData");
        var query = new Bmob.Query(Data);
        query.equalTo("professor_nyuid", nid);
        query.find({
          success: function(results) {
              var mark = 0;
            for (var i = 0; i < results.length; i++) {
              mark += results[i].get("rate");
            }
            if (!results.length) {
                callback(3);
            } else {
                mark = Math.round(mark / results.length);
                callback(mark);
            }
          },
          error: function(error) {}
        });
    }

    function refreshList(courseList) {
        let html = "";
        for (let c in courseList) {
            if (c > 20) break;

            html +=
                `<div id="btn-${courseList[c].course_id}" class="title">
                    <i class="dropdown icon"></i>
                    <b style="color: #666; font-family: sans-serif; white-space: nowrap; width: calc(100% - 30px); overflow: hidden; text-overflow: ellipsis; display: inline-block;">${courseList[c].course_title}</b>
                    <p style="padding-left: 24px; color: #AAA;">${courseList[c].term_descr} - ${courseList[c].class_type_descr}
                    <br />${"Location: " + courseList[c].location_description}</p>
                </div>
                <div class="content" style="padding: 0 0;">
                    <p id="course-${courseList[c].course_id}" class="transition hidden">
                        <i class="ui basic loading massive button disabled" style="width: 100%; margin: 5px 0px;"></i>
                    </p>
                </div>`;

        }
        $courseListBar.html(html);

        if (html) {
            $courseListBar.css("display", "block");
        } else {
            $courseListBar.css("display", "none");
        }

        for (let c in courseList) {
            if (c > 20) break;

            let cid = courseList[c].course_id;
            $(`#btn-${cid}`).on("click", function() {
                if (cid != "-1") getFaculties(cid);
            });

        }
        
    }

    function generateExtending(cid, facultyList) {
        let html = ``;

        for (let c in facultyList) {
            if (c > 20) break;

            let n = facultyList[c].instructor_name;
            let nid = facultyList[c].instructor_nyu_id;
            let color = generateColorByName(n);

            if (!nid) continue;

            html +=
                `<div id="btnp-${nid}" class="ui top bottom attached buttons">
                    <div class="ui basic button" style="padding: 5px 0px;">
                        <div class="comment">
                            <div style="margin: 5px 0px 0px 15px; width: 40px; height: 40px; background-size: cover; border-radius: 100%; display: block; margin-bottom: 5px; 
                                background: ${color}; color: ${whiteRate(color)}; opacity: .6; font-family: helvetica; line-height: 42px; font-size: 20px;">${n ? n.substr(0,1) : ""}</div>
                            <div class="content" style="width: calc(100% - 100px); display: block; text-align: left; margin: -52px 0px 0px 70px; padding: 0 0;">
                                <p style="margin: 0 0; color: #666;">${facultyList[c].instructor_name}</p>
                                <p style="margin: -3px 0 3px 0; color: #AAA; font-variant: all-petite-caps;">${facultyList[c].instructor_role_description}</p>
                                <div id="rate-${nid}" class="ui heart rating flush" data-rating="0" data-max-rating="5" style="opacity: 0.6;"></div>
                            </div>
                        </div>
                    </div>
                </div>`;

        }

        $(`#course-${cid}`).html(html);
        $('.ui.rating').rating("disable");

        for (let c in facultyList) {
            if (c > 20) break;

            let nid = facultyList[c].instructor_nyu_id;
            let n = facultyList[c].instructor_name;
            $(`#btnp-${nid}`).on("click", function() {
                window.open(`/prof.html#${nid}/${n}`, "_blank");
            });
            getRate(nid, (rate) => {
                $(`#rate-${nid}`).removeClass("flush");
                $(`#rate-${nid}`).rating("set rating", rate);
            });

        }

    }

    var current = 0;
    setInterval(function() {
        if (!$(".flush")[0]) {current = 0; return;}
        $(".flush").rating("set rating", current);
        current = (current + 1) % 6;
    }, 300);

})();
