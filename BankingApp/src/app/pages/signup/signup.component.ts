import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})
export class SignupComponent {

  signupObj: Signup;
  constructor(private http: HttpClient) {
    this.signupObj = new Signup();
  }
  onSignup() {
    this.http.post('', this.signupObj).subscribe(
    response => {
      console.log('Signup successful:', response);
    },
    error => {
      console.error('Signup failed: ', error);
    }
    );
  }
}

export class Signup {
  email: string;
  password: string;
  constructor() {
    this.email = '';
    this.password = '';
  }
}