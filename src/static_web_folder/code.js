function js_log_post(string_value){
    document.getElementById('id_div_log').innerHTML += string_value+'<br>';
}


function js_print_result(string_value){
    document.getElementById("id_stav_vypoctu").value = string_value
}


function run_python(){
    js_print_result('Progress: Passing data to python script.')

    let gui_inputs = {
        t_init: parseFloat(document.getElementById("id_Tstavba").value),
        t_in: parseFloat(document.getElementById("id_Ti0").value),
        t_out: parseFloat(document.getElementById("id_Te").value),
        duration: parseInt(document.getElementById("id_duration").value),
        concrete_thick: parseFloat(document.getElementById("id_concrThick").value),
        steel_thick: parseFloat(document.getElementById("id_steelThick").value),
        radius_in: parseFloat(document.getElementById("id_polomerVnitrni").value),
        tendons_stress: parseFloat(document.getElementById("id_sigmaP0").value),
        tendons_area: parseFloat(document.getElementById("id_plochaPredp").value),
        density: parseFloat(document.getElementById("id_density0").value),
        water_cont: parseFloat(document.getElementById("id_waterCont").value),
        therm_expan_coeff: parseFloat(document.getElementById("id_thermExpan").value),
        modulus_concrete: parseFloat(document.getElementById("id_modulusConc").value),
        modulus_steel: parseFloat(document.getElementById("id_modulusSteel").value),
        emissivity: parseFloat(document.getElementById("id_emiss").value),
        char_len: parseFloat(document.getElementById("id_Lair").value),
        pressure_ext: parseFloat(document.getElementById("id_pe").value),
        step_space: parseFloat(document.getElementById("id_Le").value),
        step_time_1: parseFloat(document.getElementById("id_dt1").value),
        step_time_2: parseFloat(document.getElementById("id_dt2").value),
        step_time_3: parseFloat(document.getElementById("id_dt3").value),
        step_time_4: parseFloat(document.getElementById("id_dt4").value),
        step_time_5: parseFloat(document.getElementById("id_dt5").value),
        poisson: parseFloat(document.getElementById("id_poisson").value)
    };

    eel.get_python_result(gui_inputs)(js_print_result)
}


eel.expose(print_status);
function print_status(string_value) {
    document.getElementById("id_stav_vypoctu").value = string_value
    js_log_post(string_value)
}
