import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../service/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent {
  loginStatus!: string;

  constructor(private authService: AuthService, private router:Router) {
  }
  onLogin(data: any) {
    const username = data.username;
    const password = data.password;
    this.authService.login(username, password).subscribe(
    response => {
      this.loginStatus = 'Login Successfully!';
      console.log('Login successful:', response);
      this.router.navigateByUrl('/dashboard');
    },
    error => {
      console.error('Login failed: ', error);
      this.loginStatus = error;
    });
  }
}