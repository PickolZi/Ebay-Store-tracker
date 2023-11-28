const MACHINE_IP = "http://localhost:5000";

const fetchFromAPIUsingEndpoint = async (endpoint) => {
    const res = await fetch(MACHINE_IP + endpoint).then((res) => {
        return res.json();
    }).then((res) => {
        return res;
    });

    return res;
}

export default fetchFromAPIUsingEndpoint;