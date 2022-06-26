import { useState } from 'react'
import plot from './graph/plot.png'

const Form = () => {

  const [show_image, setShow] = useState(false)

  const handleChange = e => {
    if (e.target.checked) {
      e.target.value = '1'
    } else {
      e.target.value = ''
    }
  }

  const onSubmit = (event) => {
    event.preventDefault()

    const days = event.target[0].value
    const company = event.target[1].value
    const learn = event.target[2].value
    const data = { days, company, learn }

    if (days == '') alert('Please enter all fields!')
    else if (days < 1 || days > 365) alert('Only values between 1 - 365 accepted!')
    else
    {
      setShow(false)
        fetch('http://localhost:5000/main', {
            'method': 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(() => {
            setShow(true)
            console.log('ADDED', data)
        }).catch((error) => {
          console.log(error)
        })
    }
  }

  return (
    <form onSubmit={onSubmit} method='POST' className='form'>
      <div>
          <input type='number' placeholder='1 - 365' name='prediction_period' className='text-field'/>
      </div>

      <div>
        <label className='text'>Choose a company:</label>
          <select name="company" className='select-field'>
            <option value="Apple,AAPL">Apple</option>
            <option value="Tesla,TSLA">Tesla</option>
            <option value="Meta,META">Meta</option>
            <option value="Microsoft,MSFT">Microsoft</option>
            <option value="Electronic Arts,EA">EA</option>
          </select>
      </div>

      <div>
        <p className='text'>Teach model again?</p>
        <input type='checkbox' name='learn' id='is_learning' onChange={handleChange} className='box_style'></input>
      </div>

      <div>
        <button 
        type='submit' 
        className='button button--pan' >
          Predict 
        </button>
      </div>

      <div>
        {(show_image == true) ? (<img src={plot} width='800'/>) : (<p>Predicting...</p>)}
      </div>
    </form>
  )
}

export default Form