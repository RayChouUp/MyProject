import {Button,DatePicker,Popup ,Field,CellGroup,TimePicker} from 'vant'
import 'vant/lib/index.css'

export default function setupVant(app) {
  app.use(Button)
  app.use(DatePicker)
  app.use(Popup)
  app.use(Field)
  app.use(CellGroup)
  app.use(TimePicker)
}