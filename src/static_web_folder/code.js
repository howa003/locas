function js_log_post(string_value){
    document.getElementById('id_div_log').innerHTML += string_value+'<br>';
}


function js_print_result(string_value){
    document.getElementById("id_stav_vypoctu").value = string_value
}


function run_python(){
    js_print_result('Progress: Passing data to python script.')

    let gui_inputs = {
        Tstavba: parseFloat(document.getElementById("id_Tstavba").value),
        Ti0: parseFloat(document.getElementById("id_Ti0").value),
        Te: parseFloat(document.getElementById("id_Te").value),
        duration: parseInt(document.getElementById("id_duration").value),
        concrThick: parseFloat(document.getElementById("id_concrThick").value),
        steelThick: parseFloat(document.getElementById("id_steelThick").value),
        polomerVnitrni: parseFloat(document.getElementById("id_polomerVnitrni").value),
        sigmaP0: parseFloat(document.getElementById("id_sigmaP0").value),
        plochaPredp: parseFloat(document.getElementById("id_plochaPredp").value),
        density0: parseFloat(document.getElementById("id_density0").value),
        waterCont: parseFloat(document.getElementById("id_waterCont").value),
        thermExpan: parseFloat(document.getElementById("id_thermExpan").value),
        modulusConc: parseFloat(document.getElementById("id_modulusConc").value),
        modulusSteel: parseFloat(document.getElementById("id_modulusSteel").value),
        emiss: parseFloat(document.getElementById("id_emiss").value),
        Lair: parseFloat(document.getElementById("id_Lair").value),
        pe: parseFloat(document.getElementById("id_pe").value),
        Le: parseFloat(document.getElementById("id_Le").value),
        dt1: parseFloat(document.getElementById("id_dt1").value),
        dt2: parseFloat(document.getElementById("id_dt2").value),
        dt3: parseFloat(document.getElementById("id_dt3").value),
        dt4: parseFloat(document.getElementById("id_dt4").value),
        dt5: parseFloat(document.getElementById("id_dt5").value),
        poisson: parseFloat(document.getElementById("id_poisson").value)
    };

    eel.get_python_result(gui_inputs)(js_print_result)
}


eel.expose(print_status);
function print_status(string_value) {
    document.getElementById("id_stav_vypoctu").value = string_value
    js_log_post(string_value)
}
