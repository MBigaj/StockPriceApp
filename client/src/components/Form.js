import { useState } from 'react'

const Form = () => {

  const [show_image, setShow] = useState(false)

  const onSubmithandler = () => {
  }

  const onSubmit = (event) => {
    event.preventDefault()

    const days = event.target[0].value
    const company = event.target[1].value
    const data = { days, company }

    if (days === '') alert('Please enter all fields!')
    else if (days < 1 || days > 365) alert('Only values between 1 - 365 accepted!')
    else
    {
      onSubmithandler()
        fetch('http://localhost:5000/main', {
            'method': 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        }).then(() => {
            console.log('ADDED', data)
        }).catch((error) => {
          console.log(error)
        })
    }
  }

  return (
    <form onSubmit={onSubmit} method='POST' className='form'>
      <div>
          <input type='number' placeholder='1 - 365' name='prediction_period' className='text-field'/> <br></br>
      </div>

      <div>
        <label className='text'>Choose a company:</label>
          <select name="company" className='select-field'>
            <option value="Apple,AAPL">Apple</option>
            <option value="Tesla,TSLA">Tesla</option>
            <option value="Meta,META">Meta</option>
            <option value="Microsoft,MSFT">Microsoft</option>
            <option value="Electronic Arts,EA">EA</option>
          </select> <br></br>
      </div>

      <div>
        <button type='submit' className='btn'>
          Predict 
        </button>
      </div>
      <img src='../../../flask-server/machine_learning/graph/plot.png'></img>
    </form>
  )
}

export default Form