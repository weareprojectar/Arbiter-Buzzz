import axios from 'axios'

function getTickerUpdated() {
    return axios.get('/api/ticker-updated')
}

function getTickerInfo(date, ticker) {
    let req_url = '/api/ticker/?date=' + date + '&code=' + ticker
    return axios.get(req_url)
}

function printTickerInfo(ticker) {
    getTickerUpdated()
      .then((response) => {
        let updatedDate = response.data.updated_date
        getTickerInfo(updatedDate, ticker)
          .then((response) => {
            console.log(response)
          })
      })
}
