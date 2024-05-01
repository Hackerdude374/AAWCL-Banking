import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../service/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent {

  constructor(private authService: AuthService, private router:Router) {
  }
  onLogin(data: any) {
    const username = data.username;
    const password = data.password;
    this.authService.login(username, password).subscribe(
    response => {
      console.log('Login successful:', response);
      this.router.navigateByUrl('/dashboard');
    },
    error => {
      console.error('Login failed: ', error);
    });
  }
}