import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, HttpClientModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  loginObj: Login;
  constructor(private http: HttpClient) {
    this.loginObj = new Login();
  }
  onLogin() {
    this.http.post('', this.loginObj).subscribe(
    response => {
      console.log('Login successful:', response);
    },
    error => {
      console.error('Login failed: ', error);
    }
    );
  }
}

export class Login {
  userId: string;
  password: string;
  constructor(){
    this.userId = '';
    this.password = '';
  }
}