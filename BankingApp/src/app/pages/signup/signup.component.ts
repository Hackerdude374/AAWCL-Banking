import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { SignupService } from '../../service/signup.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [FormsModule, CommonModule ],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})

export class SignupComponent {

  signupStatus!: string;

  constructor(private signupService: SignupService, private router: Router) { }

  onSignup(data: any) {
    const username = data.username;
    const password = data.password;
    const email = data.Email;
    const name =  data.FullName;
    const address = data.CurrAddr;
    const phone = data.PhoneNumber;
    this.signupService.signup(username, password, email, name, address, phone).subscribe(
    (response: any) => {
      console.log('Signup successful:', response);
      this.signupStatus = 'Signup Successfully!';
      this.router.navigateByUrl('/login');
    },
    (error) => {
      console.error('Signup failed: ', error);
      this.signupStatus = error;
    }
    );
  }
}
