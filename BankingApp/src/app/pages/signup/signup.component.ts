import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { SignupService } from '../service/signup.service';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})

export class SignupComponent {

  constructor(private loginService: SignupService, private router:Router) {
  }
  onSignup(data: any) {
    const username = data.username;
    const password = data.password;
    const email = data.email;
    const name = data.name;
    const address = data.address;
    const phone= data.phone;
    this.loginService.signup(username, password,email,name,address,phone).subscribe(
    response => {
      console.log('Signup successful:', response);
      this.router.navigateByUrl('/login');
    },
    error => {
      console.error('Signup failed: ', error);
    }
    );
  }
}
