const BASE_URL = "http://localhost:5000/playlists/2/search?q=rock";
// const cupcakeListEl = document.querySelector('#cupcakes-list')
// const newCupcakeFormEl = document.querySelector('#new-cupcake-form');



const response = await axios.get(`${BASE_URL}`)

console.log(response.data)