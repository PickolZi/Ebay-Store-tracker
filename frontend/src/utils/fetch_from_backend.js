import axios from 'axios';

const fetchFromAPIUsingEndpoint = async (endpoint) => {
    const res = await axios.get(endpoint).then(async (res) => {
        return res.data;
    })

    return res;
}

export default fetchFromAPIUsingEndpoint;